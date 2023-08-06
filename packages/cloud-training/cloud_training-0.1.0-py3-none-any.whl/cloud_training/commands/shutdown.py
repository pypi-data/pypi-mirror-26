from cloud_training.project_command import ProjectCommand


class ShutdownCommand(ProjectCommand):

    def run(self):
        instances = self._aws.get_instances_by_tag('model', '%s-%s' % (self._project_config['project_name'], self._model))
        if not instances:
            self._print('Running instances for this model were not found.')
            return True

        instances_ids = []
        for instance in instances:
            instances_ids.append(instance['InstanceId'])

        confirm = input('Instances to terminate: %s (type "y" to confirm): ' % ', '.join(instances_ids))
        if confirm != 'y':
            self._print('You didn\'t confirm the operation.')
            return True

        res = self._aws.terminate_instances(instances_ids)
        if not res:
            self._print('Something went wrong. Please check the statuses of instances manually.')
            return False

        self._print('Instances are shutting-down.')

        return True
