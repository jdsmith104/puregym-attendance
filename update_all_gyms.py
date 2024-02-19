import puregym
import json

def main(email: str, pin: str):
    
    client = puregym.PuregymAPIClient()
    client.login(email, pin)

    all_gyms = client.get_list_of_gyms()

    if all_gyms:
        # Convert and write JSON object to file
        with open("all_gyms.json", "w") as outfile: 
            json.dump(all_gyms, outfile,indent=4, sort_keys=True)

if __name__ == "__main__":
    print("Getting all gyms")

    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    
    email = credentials.get("email")
    pin = credentials.get("pin")
    print(f"Credentials email={email} pin={pin}")

    main(email, pin)
