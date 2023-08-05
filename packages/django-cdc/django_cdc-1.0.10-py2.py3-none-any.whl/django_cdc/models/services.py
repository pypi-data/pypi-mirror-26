import json
import logging
from datetime import datetime, time

from django.db.models.fields.files import ImageFieldFile

from constants import ServiceType
from django_cdc import settings
from . import lambda_client, kinesis_client, sns_client, sns_arn
import uuid

logger = logging.getLogger(__name__)

try:
    from django.utils.timezone import now as datetime_now
    from bitfield.types import BitHandler
    assert datetime_now
    assert BitHandler
except ImportError:
    from datetime import datetime
    BitHandler = object.__class__
    datetime_now = datetime.now


class Service(object):
    def factory(type):
        if type == ServiceType.KINESIS:
            return kinesis_service()
        elif type == ServiceType.SNS:
            return SNS_service()
        elif type == ServiceType.LAMBDA_KINESIS:
            return lambda_service()
        else:
            return
        assert 0, "Bad Service Request: " + type

    factory = staticmethod(factory)


class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile) or isinstance(obj, datetime) \
                or isinstance(obj, time) or isinstance(obj, BitHandler):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class CommonUtils(object):
    def get_function_name(self, table_name):
        function_name = "{0}{1}{2}".format(settings.LAMBDA_FUNCTION_PREFIX,
                                           "-",
                                           table_name)
        return function_name


class lambda_service(object):
    common_utils = CommonUtils()

    def put_data_entry(self, name, *args, **kwargs):
        '''create lambda function which pushes data to kinesis '''
        function_name = self.common_utils.get_function_name(name)
        payload_json = json.dumps(args, cls=PythonObjectEncoder)
        logger.info("My Data :%s", payload_json)
        try:
            lambda_client.invoke(FunctionName=function_name,
                                 InvocationType='Event',
                                 Payload=payload_json)

        except Exception as e:
            logger.error("Error Occured while invoking lambda"
                         " function %s" % str(e))

    def get_serverless_func(self, lambda_name):
        function_val = {'name': lambda_name,
                        'handler': 'handler.push_data_to_kinesis',
                        'environment': {
                            'KINESIS_STREAM': lambda_name,
                            'AWS_REGION_NAME': settings.AWS_REGION_NAME}}
        return function_val


class kinesis_service(object):
    '''publish data directly on kinesis'''
    common_utils = CommonUtils()

    def put_data_entry(self, name, *args, **kwargs):
        try:
            kinesis_stream = self.common_utils.get_function_name(name)
            records = []
            logger.info("My Data :%s", args)
            for package in args:
                record = {
                    'Data': json.dumps(package, cls=PythonObjectEncoder),
                    'PartitionKey': str(uuid.uuid4())}
                records.append(record)
            response = kinesis_client.put_records(Records=records,
                                                  StreamName=kinesis_stream)
            print response
        except Exception as e:
            logger.error(
                "Error Occurred while pushing data to kinesis %s" % str(e))


class SNS_service(object):
    '''publish data directly on sns'''
    common_utils = CommonUtils()

    def put_data_entry(self, name, *args, **kwargs):
        try:
            logger.info("My Data :%s", args)
            function_name = self.common_utils.get_function_name(name)
            arn = "{0}{1}".format(sns_arn, function_name)
            sns_client.publish(TargetArn=arn,
                               Message=json.dumps({
                                   'default':
                                       json.dumps(args,
                                                  cls=PythonObjectEncoder)
                               }),
                               MessageStructure='json')
        except Exception as e:
            logger.error(
                "Error Occurred while pushing data to SNS %s" % str(e))
