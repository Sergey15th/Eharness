[![Continous integration](https://github.com/frePPLe/frepple/actions/workflows/ubuntu24.yml/badge.svg)](https://github.com/frePPLe/frepple/actions/workflows/ubuntu24.yml)

# frePPLe

## Open source supply chain planning

FrePPLe is an easy-to-use and easy-to-implement open source **demand forecasting** and
**advanced planning and scheduling** tool for manufacturing companies.

When spreadsheets doesn't suffice any longer to adequately plan and schedule your production, frePPLe allows an easy and cost-efficient way to generate a more optimized plan.

FrePPLe implements time series forecasting algorithms to analyze the sales history and compute the forecasted sales for the future.

FrePPLe implements production planning and scheduling algorithms based on best practices such as **theory of constraints** (ie *plan around the bottleneck*), **pull-based planning** (ie *start production as late as possible and directly triggered by demand*) and **lean manufacturing** (ie *avoid intermediate delays and inventory*).

## Download

The software can be downloaded in the following formats:

* Ubuntu 24 .deb package on https://github.com/frePPLe/frepple/releases/
* Docker container on https://github.com/orgs/frePPLe/packages/container/package/frepple-community
* Source tarball or zip file from https://github.com/frePPLe/frepple/releases/
* Documentation zip file from https://github.com/frePPLe/frepple/releases/

## Documentation

Visit [https://frepple.com](https://frepple.com) for documentation, screencasts and build instructions.

## License

The *Community Edition* is released under the [MIT licence](https://opensource.org/license/mit/).

The *Enterprise Edition* can be purchased from frePPLe bv. It provides additional functionality
and professional support.

The *Cloud Edition* provides provides the same capabilities as the Enterprise Edition, but is
hosted as a service in the cloud: fully supported and maintained by frePPLe bv.

## Celery integration

This project includes an optional Celery integration to run background tasks.

Configuration
- Set the broker and backend using environment variables, for example:
	- `FREPPLE_CELERY_BROKER_URL=redis://localhost:6379/0`
	- `FREPPLE_CELERY_RESULT_BACKEND=redis://localhost:6379/1`

Running a worker

- Activate the virtualenv and install requirements (if needed).
- Start a worker from the project root:

	```powershell
	& .\venv\Scripts\Activate.ps1; celery -A freppledb worker -l info
	```

Starting periodic tasks (beat)

	```powershell
	& .\venv\Scripts\Activate.ps1; celery -A freppledb beat -l info
	```

Testing tasks

- You can call tasks from Django shell or code, e.g.:

	```python
	from freppledb.common.tasks import example_add
	example_add.delay(1, 2)
	```

If you prefer another broker (RabbitMQ, SQS, etc.) set the appropriate broker URL.
