import os
import unittest

from dotenv import load_dotenv

from src.utils.enums.information_type import InformationType
from src.task.task_spec import TaskSpec

load_dotenv()


class TestTaskSpec(unittest.TestCase):
    def setUp(self):
        self.task_spec_path = os.getenv('TASK_SPEC_FOR_DRAW_MORE_INFO_PATH')
        with open(self.task_spec_path) as fp:
            self.task_spec_str = fp.read()

    def test_init_with_task_spec_str(self):
        task_spec = TaskSpec(task_spec_str=self.task_spec_str)
        self._validate(task_spec)

    def test_init_with_task_spec_path(self):
        task_spec = TaskSpec(task_spec_path=self.task_spec_path)
        self._validate(task_spec)

    def _validate(self, task_spec: TaskSpec):
        self.assertEqual(task_spec.name, 'draw_more_info')
        self.assertTrue(
            'The current objective is {current_objective}.' in task_spec.task_prompt_template)
        self.assertEqual(task_spec.system_prompt_template, '')
        self.assertEqual(len(task_spec.input_information_names), 3)
        self.assertTrue('information_queue_names' in task_spec.parsed_output_information_spec.keys())
        self.assertEqual(
            task_spec.parsed_output_information_spec['information_queue_names']['information_type'],
            InformationType.ARRAY)
        self.assertEqual(task_spec.action_names[0], 'do_draw_information_from_queue')


if __name__ == '__main__':
    unittest.main()
