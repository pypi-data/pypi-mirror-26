#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import signal

import click
from apscheduler.schedulers.background import BackgroundScheduler

import agent
import agent.config as config
import agent.qualityplatform.api as server_api
from agent.consts import AgentStatus
from agent.server.api import start_server

logger = logging.getLogger(__name__)
agent_id = 0

scheduler = BackgroundScheduler()
logging.getLogger("apscheduler").setLevel(logging.ERROR)


def output_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: %s" % agent.__version__)
    ctx.exit()


@click.command()
@click.option(
    '-v',
    '--version',
    is_flag=True,
    is_eager=True,
    callback=output_version,
    expose_value=False,
    help="show the version of this tool")
@click.option(
    '-e',
    '--environment',
    default='prod',
    help='select a development environment such as alpha|beta|prod')
def parse_command(environment):
    config.qualityplatform['api_url'] = config.qualityplatform_env_api_url.get(environment)
    config.sentry_url['url'] = config.sentry_env_url.get(environment)
    logger.info(config.sentry_url.get('url'))
    config.agent['port'] = config.agent_env_port.get(environment)
    start_agent_client()


def check_devices(status):
    return server_api.register_agent(status)


def check_devices_cron():
    server_api.register_agent(AgentStatus.online.value)


def signal_handler(signum, frame):
    server_api.unregister_agent(config.agent['agent_id'])
    scheduler.shutdown()


def start_agent_client():
    agent_data = check_devices(AgentStatus.online.value)
    if agent_data:
        config.agent['agent_id'] = agent_data.get('id')
    signal.signal(signal.SIGINT, signal_handler)
    scheduler.add_job(check_devices_cron, 'interval', seconds=15)
    scheduler.start()
    start_server()


def main():
    print("A Terminal Tools For agent Agent")
    parse_command()


if __name__ == "__main__":
    main()
