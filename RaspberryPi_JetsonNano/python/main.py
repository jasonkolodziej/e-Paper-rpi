


from src import SystemStatus


if __name__ == '__main__':
    s = SystemStatus()
    # s.generate_qr()
    print(s.to_json())