import olca as ipc


def main():
    client = ipc.Client(8080)
    (data, _) = client.rpc_call('get/models', {'@type': 'UnitGroup'})
    print(data)


if __name__ == '__main__':
    main()
