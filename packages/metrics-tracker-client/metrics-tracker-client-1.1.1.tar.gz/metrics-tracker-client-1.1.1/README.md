# Overview

Metrics Collector Service collects statistics for deployment of a github sample code on Cloud Foundry, Kubernetes, Data Science Experience, OpenWhisk etc.

This is the source code for metrics_tracker_client, a pip package that can track and report details of a demo/tutorial.

## How To Use It On Applications

1. Open a terminal and run

   ```bash
   pip install metrics-tracker-client
   ```
2. Import the package at the entry point of your app and call the `track()` function.

    ```python
    import metrics_tracker_client
    metrics_tracker_client.track()
    ```
3. Add a copy of the Privacy Notice to the readme file. 

   **Note:** All apps that have deployment tracker must include the Privacy Notice.

4. Add a `repository.yaml` file in the same directory of your main entry point files.

## How To Use It On Jupyter Notebook

1. In your Jupyter Notebook, insert the following code in your entry point code block. Then, fill in the parameter in `metrics_tracker_client.DSX()` with the format `'<gitHub Organization>/<Repository name>'`.

	```python
	!pip install -q metrics-tracker-client
	import metrics_tracker_client
	metrics_tracker_client.DSX('org/repo')
	```

2. Add a copy of the Privacy Notice to the readme file. 

   **Note:** All apps that have deployment tracker must include the Privacy Notice.

3. Add a `repository.yaml` file in your GitHub's top-level repository.

## Example repository.yaml file

The repository.yaml need to be written in Yaml format. Also, please put all your keys in lower case.

```yaml
id: watson-discovery-news
runtimes: 
  - Cloud Foundry
services: 
  - Discovery
event_id: web
event_organizer: dev-journeys
language: python
```

Required field:

1. id: Put your journey name/Github URL of your journey.
2. runtimes: Put down all your platform runtime environments in a list.
3. services: Put down all the bluemix services that are used in your journey in a list.
4. event_id: Put down where you will distribute your journey. Default is web.
5. event_organizer: Put down your event organizer if you have one.
6. language: If your journey is not in **python**, please put down the journey's main language in lower case.


## Example app

To see how to include this into your app please visit [watson-online-store](https://github.com/IBM/watson-online-store). You will want to pay attention to [repository.yaml](https://github.com/IBM/watson-online-store/blob/master/repository.yaml) and [run.py](https://github.com/IBM/watson-online-store/blob/master/run.py#L184).

To see how to include this into your Jupyter Notebook please visit [Integrate-Investment-Portfolio](https://github.com/IBM/Integrate-Investment-Portfolio). You will want to pay attention to [repository.yaml](https://github.com/IBM/Integrate-Investment-Portfolio/blob/master/repository.yaml) and [SetupPortfolio.ipynb](https://github.com/IBM/Integrate-Investment-Portfolio/blob/master/notebooks/SetupPortfolio.ipynb).

## Privacy Notice

Sample web applications that include this package may be configured to track deployments to [IBM Bluemix](https://www.bluemix.net/) and other platforms. The following information is sent to a [Deployment Tracker](https://github.com/IBM/metrics-collector-service) service on each deployment:

* Python package version
* Python repository URL
* Application Name (`application_name`)
* Application GUID (`application_id`)
* Application instance index number (`instance_index`)
* Space ID (`space_id`) or OS username
* Application Version (`application_version`)
* Application URIs (`application_uris`)
* Cloud Foundry API (`cf_api`)
* Labels of bound services
* Number of instances for each bound service and associated plan information
* Metadata in the repository.yaml file

This data is collected from the `setup.py` and `repository.yaml` file in the sample application and the `VCAP_APPLICATION` and `VCAP_SERVICES` environment variables in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix to measure the usefulness of our examples, so that we can continuously improve the content we offer to you. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

## Disabling Deployment Tracking

Please see the README for the sample application that includes this package for instructions on disabling deployment tracking, as the instructions may vary based on the sample application in which this package is included.

## License

See [License.txt](License.txt) for license information.
