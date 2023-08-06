# Copyright 2017 Bracket Computing, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# https://github.com/brkt/brkt-cli/blob/master/LICENSE
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and
# limitations under the License.

from brkt_cli.aws import aws_args


def setup_wrap_image_args(parser, parsed_config):
    parser.add_argument(
        'ami',
        metavar='ID',
        help='The guest AMI that will be launched as a wrapped Bracket instance'
    )
    parser.add_argument(
        '--stock-image-version',
        metavar='STOCK_IMAGE_VERSION',
        help='The version number when specifying "ubuntu" or "centos" instead of'
             ' an AMI ID. The default versions are Ubuntu 16.04 and CentOS 7.'
    )
    parser.add_argument(
        '--wrapped-instance-name',
        metavar='NAME',
        dest='wrapped_instance_name',
        help='Specify the name of the wrapped Bracket instance',
        required=False
    )
    parser.add_argument(
        '--instance-type',
        metavar='TYPE',
        dest='instance_type',
        help='The instance type to use when launching the wrapped image',
        default='m4.large'
    )
    aws_args.add_no_validate(parser)
    aws_args.add_region(parser, parsed_config)
    aws_args.add_security_group(parser, parsed_config)
    aws_args.add_subnet(parser, parsed_config)
    aws_args.add_aws_tag(parser)
    aws_args.add_metavisor_version(parser)
    aws_args.add_key(parser, help='SSH key pair name')

    # Optional AMI ID that's used to launch the encryptor instance.  This
    # argument is hidden because it's only used for development.
    aws_args.add_encryptor_ami(parser)

    # Optional IAM role for the instance
    parser.add_argument(
        '--iam',
        metavar='ROLE',
        dest='iam',
        help='The IAM role to use for the launched instance',
    )
    # Optional arguments for changing the behavior of our retry logic.  We
    # use these options internally, to avoid intermittent AWS service failures
    # when running concurrent encryption processes in integration tests.
    aws_args.add_retry_timeout(parser)
    aws_args.add_retry_initial_sleep_seconds(parser)
