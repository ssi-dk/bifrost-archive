. activate bifrost
uwsgi -s /tmp/reporter.sock --manage-script-name --mount /=reporter:application --http :8050
