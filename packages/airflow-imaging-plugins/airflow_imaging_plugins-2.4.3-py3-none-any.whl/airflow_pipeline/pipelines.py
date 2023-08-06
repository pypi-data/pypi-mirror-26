import logging

from airflow.settings import Session
from airflow.models import DagRun

from datetime import datetime
from textwrap import dedent

from data_tracking.files_recording import create_provenance, visit


PIPELINE_XCOMS = ['root_folder',            # root folder, usually provided by user
                  'folder',                 # for incoming XCOMs: input folder, for outgoing XCOMs: output folder
                  'relative_context_path',  # relative path from the folder up to the root folder
                  'metadata_folder',        # folder containing extra metadata for the images
                  'session_id',
                  'output',                 # output logs
                  'error',                  # error logs
                  'dataset',                # name of the dataset under processing
                  'matlab_version',
                  'spm_version',
                  'spm_revision',
                  'provenance_details',
                  'provenance_previous_step_id']


def pipeline_trigger(parent_task):
    """Generates a trigger function attached to a parent task."""

    def trigger(context, dag_run_obj):
        """
        Trigger function.

        Use this function with TriggerDagRunOperator to always trigger a DAG and
        pass pipeline information to the next DAG
        """

        ti = context['task_instance']
        dr = context['dag_run']
        dag_run_obj.payload = dict()
        for key in PIPELINE_XCOMS:
            dag_run_obj.payload[key] = ti.xcom_pull(
                task_ids=parent_task, key=key)
            if (not dag_run_obj.payload[key]) and key in dr.conf:
                dag_run_obj.payload[key] = dr.conf[key]
        return dag_run_obj

    return trigger


class TransferPipelineXComs(object):

    def __init__(self, parent_task, dataset_config, organised_folder):
        self.parent_task = parent_task
        self.dataset_config = dataset_config
        self.pipeline_xcoms = dict()
        self.organised_folder = organised_folder
        self.incoming_parameters = dedent("""
          # Task {{ task.task_id }}
          Parent task = $parent_task

          ## Incoming parameters
          dataset = {{ task_instance.xcom_pull(task_ids='$parent_task', key='dataset') }}
          folder = {{ task_instance.xcom_pull(task_ids='$parent_task', key='folder') }}
          {%  set session_id = task_instance.xcom_pull(task_ids='$parent_task', key='session_id') -%}
          {%- if session_id %}
          session_id = {{ session_id }}
          {%  endif -%}
          {%  set metadata_folder = task_instance.xcom_pull(task_ids='$parent_task', key='metadata_folder') -%}
          {%- if metadata_folder %}
          metadata_folder = {{ metadata_folder }}
          {%  endif -%}
          {%- set scan_date = task_instance.xcom_pull(task_ids='$parent_task', key='scan_date') -%}
          {%- if scan_date %}
          scan_date = {{ scan_date }}
          {%  endif %}

          {%-  set matlab_version = task_instance.xcom_pull(task_ids='$parent_task', key='matlab_version') -%}
          {%- set spm_version = task_instance.xcom_pull(task_ids='$parent_task', key='spm_version') -%}
          {%- set spm_revision = task_instance.xcom_pull(task_ids='$parent_task', key='spm_revision') -%}
          {%- set provenance_details = task_instance.xcom_pull(task_ids='$parent_task', key='provenance_details') -%}
          {%- if matlab_version or spm_version %}
          ## Provenance information
          matlab_version = {{ matlab_version }}
          spm_version = {{ spm_version }}
          spm_revision = {{ spm_revision }}
          provenance_details = {{ provenance_details }}

          {%  endif -%}
          {%- set output = task_instance.xcom_pull(task_ids='$parent_task', key='output') -%}
          {%- set error = task_instance.xcom_pull(task_ids='$parent_task', key='error') -%}
          {%- if output or error %}
          ## Output from previous task $parent_task

          ### Output
          {{ output }}

          ### Errors
          {{ error }}

          {% endif %}
        """.replace("$parent_task", parent_task))

    def read_pipeline_xcoms(self, context, expected=None):
        expected = expected or []
        for xcom in PIPELINE_XCOMS:
            value = self.xcom_pull(
                context, task_ids=self.parent_task, key=xcom)
            if value:
                self.pipeline_xcoms[xcom] = value
            elif xcom in expected:
                logging.warning("xcom argument '%s' is empty", xcom)
        self.pipeline_xcoms['task_id'] = self.task_id
        if 'session_id' not in self.pipeline_xcoms:
            dr = context['dag_run']
            if 'session_id' in dr.conf:
                self.pipeline_xcoms['session_id'] = dr.conf['session_id']

    def write_pipeline_xcoms(self, context):
        for key, value in self.pipeline_xcoms.items():
            logging.debug("Write XCOM %s=%s", key, value)
            context['ti'].xcom_push(key=key, value=value)

    def track_provenance(self, output_folder, software_versions=None):
        provenance_id = create_provenance(self.pipeline_xcoms['dataset'], software_versions=software_versions)
        provenance_step_id = visit(output_folder, provenance_id, self.task_id,
                                   previous_step_id=self.previous_step_id(),
                                   config=self.dataset_config,
                                   is_organised=self.organised_folder)
        self.pipeline_xcoms['provenance_previous_step_id'] = provenance_step_id

    def trigger_dag(self, context, dag_id, output, error=''):
        if dag_id:
            run_id = 'trig__' + datetime.now().isoformat()
            payload = {
                'output': output,
                'error': error
            }
            payload.update(self.pipeline_xcoms)

            session = Session()
            dr = DagRun(
                dag_id=dag_id,
                run_id=run_id,
                conf=payload,
                external_trigger=True)
            session.add(dr)
            session.commit()
            session.close()

    def previous_step_id(self):
        psid = self.pipeline_xcoms['provenance_previous_step_id']
        if psid == '-1':
            return None
        else:
            return int(psid)
