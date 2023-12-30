# Importing necessary libraries and functions #
#=============================================#
# Typing
from typing  import Dict
# RestAPI Lib
from fastapi import APIRouter, Depends, HTTPException
# Functions
from vauth import login , VAuth
from multiapi_routes.Libs.check      import check_wallet, check_rules

# DB 
from multiapi_routes.Libs.DB import Wallet


class Wallets(APIRouter):

    permissions = {
        "all"  : "wallet.{}",
        "read" : "wallet.read.{}",
        "create" : "wallet.create.{}",
        "update" : "wallet.update.{}",
        "delete" : "wallet.delete.{}"
    }

    def __init__(self, *args, **kwargs):
        self.name = "wallet"
        self.global_local = "wallet.*"
        super().__init__(*args, **kwargs)

        print(VAuth().register_permission("wallet",["read","create","update","delete"],True))
        # Adding routes for different HTTP methods
        self.add_api_route("/wallets", self.read_items, methods=["GET"], dependencies=[Depends(login)])
        self.add_api_route("/wallets", self.create_item, methods=["POST"], dependencies=[Depends(login)])
        self.add_api_route("/wallets", self.update_item, methods=["PUT"], dependencies=[Depends(login)])
        self.add_api_route("/wallets", self.delete_item, methods=["DELETE"], dependencies=[Depends(login)])


    def read_items(self, token: str = Depends(login), id: str = ""):
        permission = [self.permissions["all"].format("*"),self.permissions["read"].format("*")]
        # If id is not provided, return all items
        if id == "":
            if Wallet.find().count() == 0:
                raise HTTPException(status_code=404, detail="No items found.")
            items = []
            for _ in Wallet.find().all():
                temp = permission.copy()
                temp.append(self.permissions["read"].format(_.id))
                temp.append(self.permissions["all"].format(_.id))
                if token.has_permission(temp):
                    if _.author == token.token:
                        items.append(_)
            if not items:
                raise HTTPException(status_code=404, detail="No items found.")
            return items
        else:
            if not check_wallet(id):
                raise HTTPException(status_code=404, detail=f"Wallet with id {id} doesn't exist!")
            permission.append(self.permissions["read"].format(id))
            permission.append(self.permissions["all"].format(id))
            if not token.has_permission(permission):
                raise HTTPException(status_code=403, detail="Your token isn't allowed to perform this action.")
            # If id is provided, return the item with the given id
            item = Wallet.find(Wallet.id == id).first()
            if item.author != token.token:
                raise HTTPException(status_code=403, detail="Your token isn't allowed to perform this action.")
            return item
    
    def create_item(self, wallet : Dict, token: str = Depends(login)):
        permission = [self.permissions["all"].format("*"),self.permissions["create"].format("*")]
        # Define the rules for the wallet model
        parameters = ["key_wallet"]
        # Check if all required parameters are wallet
        rule_check = check_rules(rule_list=parameters, row_rest=wallet)
        if rule_check is not True:
            raise HTTPException(status_code=400, detail=f"Missing or invalid parameters: {rule_check}")
        if not token.has_permission(permission):
            raise HTTPException(status_code=403, detail="Your token isn't allowed to perform this action.")
        if Wallet.find(Wallet.author == token.token).count() != 0:
            raise HTTPException(status_code=403, detail="You already have a wallet!")
        wallet.update({"author":token.token})
        item = Wallet(**wallet)
        item.save()
        if not token.has_permission(f"{self.name}.{item.id}"):
            VAuth().add_permission(self.name,item.id)
            token.add_permission(f"{self.name}.{item.id}")
        return item
    
    def update_item(self, new_key : Dict, token: str = Depends(login)):
        permission = [self.permissions["all"].format("*"),self.permissions["update"].format("*")]
        # Define the rules for the wallet model
        item = Wallet.find(Wallet.author == token.token).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"You don't have a wallet!")
        if not token.has_permission(permission):
            raise HTTPException(status_code=403, detail="Your token isn't allowed to perform this action.")
        permission.append(self.permissions["update"].format(item.id))
        permission.append(self.permissions["all"].format(item.id))
        item.key_wallet.update(new_key)
        item.save()
        return item
    
    def delete_item(self, id : str, token: str = Depends(login)):
        permission = [self.permissions["all"].format("*"),self.permissions["delete"].format("*")]
        if not check_wallet(id):
            raise HTTPException(status_code=404, detail=f"Wallet with id {id} doesn't exist!")
        permission.append(self.permissions["delete"].format(id))
        permission.append(self.permissions["all"].format(id))
        if not token.has_permission(permission):
            raise HTTPException(status_code=403, detail="Your token isn't allowed to perform this action.")
        item = Wallet.find(Wallet.author == token.token).first()
        if id == "all":
            item.key_wallet = {}
            item.save()
        elif id in item.key_wallet.keys():
            del item.key_wallet[id]
            item.save()
        else:
            raise HTTPException(status_code=404, detail=f"Wallet key id {id} doesn't exist!")
        return {"info":f"Wallet ({id}) Deleted!","status":"Success"}