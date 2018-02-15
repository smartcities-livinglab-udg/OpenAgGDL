def generate_config(api_url=None):
    config =  {
        "httpd": {
            "port": "5984",
            "bind_address": "0.0.0.0",
            "enable_cors": "true",
        },
        "cors": {
            "origins": "*",
            "credentials": "true",
        },
        "query_server_config": {
            "reduce_limit": "false"
        },
        "compactions": {
            "_default": "[{db_fragmentation, \"40%\"}, {view_fragmentation, \"30%\"}, {from, \"23:00\"}, {to, \"06:00\"}]"
        },
        "compaction_daemon": {
            "check_interval": "300",
            "min_file_size": "131072"
        }
    }
    if api_url:
        config["httpd_global_handlers"] = {
            "_openag": "{{couch_httpd_proxy, handle_proxy_req, <<\"{}\">>}}".format(api_url)
        }
    return config
