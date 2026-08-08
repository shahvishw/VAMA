from assistant import VamaAssistant

def main():

    vama = VamaAssistant()

    print("-"*20)
    print("===== VAMA STARTED =====")
    print("type 'exit' to quite")

    while True:
        command = input("You : ")

        response = vama.process(command)

        print('VAMA : ',response)

        if command.lower().strip() in ('exit','bye'):
            break

if __name__ == '__main__':
    main()