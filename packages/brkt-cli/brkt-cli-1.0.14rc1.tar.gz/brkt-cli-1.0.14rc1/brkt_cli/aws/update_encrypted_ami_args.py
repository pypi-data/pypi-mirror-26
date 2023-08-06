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


def setup_update_encrypted_ami(parser, parsed_config):
    parser.add_argument(
        'ami',
        metavar='ID',
        help='The encrypted AMI that will be updated'
    )
    parser.add_argument(
        '--encrypted-ami-name',
        metavar='NAME',
        dest='encrypted_ami_name',
        help='Specify the name of the generated encrypted AMI',
        required=False
    )
    parser.add_argument(
        '--guest-instance-type',
        metavar='TYPE',
        dest='guest_instance_type',
        help='The instance type to use when running the encrypted guest '
             'instance',
        default='m4.large'
    )
    parser.add_argument(
        '--updater-instance-type',
        metavar='TYPE',
        dest='updater_instance_type',
        help='The instance type to use when running the updater instance',
        default='m4.large'
    )
    aws_args.add_no_validate(parser)
    aws_args.add_region(parser, parsed_config)
    aws_args.add_security_group(parser, parsed_config)
    aws_args.add_subnet(parser, parsed_config)
    aws_args.add_key(parser)
    aws_args.add_aws_tag(parser)
    aws_args.add_metavisor_version(parser)
    aws_args.add_encryptor_ami(parser)
    aws_args.add_retry_timeout(parser)
    aws_args.add_retry_initial_sleep_seconds(parser)
