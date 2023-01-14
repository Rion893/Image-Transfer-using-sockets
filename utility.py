def wait_for_acknowledge(client,response):
    amount_received = 0
    amount_expected = len(response)
    
    msg = str()
    while amount_received < amount_expected:
        data = client.recv(16)
        amount_received += len(data)
        msg += data.decode("utf-8")
    return msg