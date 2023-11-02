import json
import base64

json_string = """
{
  "end_device_ids": {
    "device_id": "eui-8cf95720000b8c4c",
    "application_ids": {
      "application_id": "ifempto"
    },
    "dev_eui": "8CF95720000B8c4C",
    "join_eui": "526973696E674846",
    "dev_addr": "27FEC4E0"
  },
  "correlation_ids": [
    "as:up:01H4SAVR3F27R7QPEW528RMG90",
    "gs:conn:01H4PRZPN00AYB3D775NJSX9WQ",
    "gs:up:host:01H4PRZPSHD3X9KS955TEJYTB7",
    "gs:uplink:01H4SAVQMHQTPD4ECWKKAAEJK8",
    "ns:uplink:01H4SAVQRR9S1T1SEDHZFFZPBB",
    "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01H4SAVQMJE7FZBJEHGPZJ9TFE",
    "rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01H4SAVQZ81ZEPY3HD82SXVK1W"
  ],
  "received_at": "2023-07-07T23:26:43.311672343Z",
  "uplink_message": {
    "session_key_id": "AYkkhB9u5MvKvGvIALeVQA==",
    "f_port": 25,
    "f_cnt": 15,
    "frm_payload": "gQqQHyErAwAAAAAC/g==",
    "rx_metadata": [
      {
        "gateway_ids": {
          "gateway_id": "eui-7076ff007906001d",
          "eui": "7076FF007906001D"
        },
        "time": "2023-07-07T23:26:42.778506Z",
        "timestamp": 483883061,
        "rssi": -79,
        "channel_rssi": -79,
        "snr": 12.5,
        "uplink_token": "CiIKIAoUZXVpLTcwNzZmZjAwNzkwNjAwMWQSCHB2/wB5BgAdELXw3eYBGgwIsr6ipQYQwMzDjQMgiJ62zYrVEg==",
        "channel_index": 7,
        "received_at": "2023-07-07T23:26:42.833676864Z"
      }
    ],
    "settings": {
      "data_rate": {
        "lora": {
          "bandwidth": 125000,
          "spreading_factor": 7,
          "coding_rate": "4/5"
        }
      },
      "frequency": "903700000",
      "timestamp": 483883061,
      "time": "2023-07-07T23:26:42.778506Z"
    },
    "received_at": "2023-07-07T23:26:42.968163015Z",
    "consumed_airtime": "0.066816s",
    "network_ids": {
      "net_id": "000013",
      "tenant_id": "scalldigital",
      "cluster_id": "nam1",
      "cluster_address": "nam1.cloud.thethings.industries",
      "tenant_address": "scalldigital.nam1.cloud.thethings.industries"
    }
  }
}
"""

json_obj = json.loads(json_string)

# Print device_id
print(json_obj["end_device_ids"]["device_id"])

# Print frm_payload
raw_payload = json_obj["uplink_message"]["frm_payload"]
print(raw_payload)
print(base64.b64decode(raw_payload).hex())