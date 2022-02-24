# user_deposit = APIRouter()

# @user_deposit.post("/")
# async def create__deposit(
#     deposit_details: UserDeposit, user: dict = Depends(UserMixin.authenticate_user)
# ):
#     try:
#         ## MAKE A REQUEST TO VERIFY PAYMENT with payment_ref
#         user_account = Deposit.get_user_account(userId=user["id"])
#         if user_account:
#             current_balance = user_account.total_amount + deposit_details.total_amount
#             user_account.update(total_amount=current_balance)
#             user_account.save(clean=True)
#             return Fortauto.response(
#                 {
#                     "message": f"You account credited with ₦{deposit_details.total_amount}"
#                 },
#                 status_code=status.HTTP_201_CREATED,
#             )
#         deposit = Deposit(
#             total_amount=deposit_details.total_amount, userId=user["id"]
#         ).save(clean=True)
#         if deposit:
#             return Fortauto.response(
#                 {
#                     "message": f"You account credited with ₦{deposit_details.total_amount}"
#                 },
#                 status_code=status.HTTP_201_CREATED,
#             )
#         return Fortauto.response(
#             {"message": "error making deposit"}, status_code=status.HTTP_400_BAD_REQUEST
#         )
#     except errors.ValidationError:
#         return Fortauto.response(
#             {"message": "error validating payment details"},
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )
#     except Exception.__base__:
#         return Fortauto.response(
#             {"message": "error making depositing"},
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )

# @user_deposit.put("/")
# async def update_user_deposit_account(
#     deposit_details: UpdateDeposit, user: dict = Depends(UserMixin.authenticate_user)
# ):
#     if user["super_admin"]:
#         try:
#             user_account = Deposit.get_user_account(userId=deposit_details.userId)
#             if user_account:
#                 if (
#                     deposit_details.method.lower() == "credit"
#                     and deposit_details.total_amount > 0
#                 ):
#                     current_balance = (
#                         user_account.total_amount + deposit_details.total_amount
#                     )
#                     user_account.update(total_amount=current_balance)
#                     user_account.save(clean=True)
#                     return Fortauto.response(
#                         {
#                             "message": f"Your account was credited with ₦{deposit_details.total_amount}"
#                         },
#                         status_code=status.HTTP_200_OK,
#                     )
#                 elif (
#                     deposit_details.method.lower() == "debit"
#                     and deposit_details.total_amount > 0
#                 ):
#                     if user_account.total_amount < deposit_details.total_amount:
#                         balance = (
#                             deposit_details.total_amount - user_account.total_amount
#                         )
#                         return Fortauto.response(
#                             {
#                                 "message": f"user does not have sufficient amount, required ₦{balance} to complete transaction"
#                             },
#                             status_code=status.HTTP_400_BAD_REQUEST,
#                         )
#                     current_balance = (
#                         user_account.total_amount - deposit_details.total_amount
#                     )
#                     user_account.update(total_amount=current_balance)
#                     user_account.save(clean=True)
#                     return Fortauto.response(
#                         {
#                             "message": f"Your account was debited with ₦{deposit_details.total_amount}"
#                         },
#                         status_code=status.HTTP_200_OK,
#                     )
#                 if (
#                     deposit_details.method.lower() != "debit"
#                     and deposit_details.method != "credit"
#                 ):
#                     return Fortauto.response(
#                         {"message": "deposit method not recognized"},
#                         status_code=status.HTTP_400_BAD_REQUEST,
#                     )
#                 elif deposit_details.total_amount <= 0:
#                     return Fortauto.response(
#                         {"message": "you can only deposit amount greater than ₦100 "},
#                         status_code=status.HTTP_400_BAD_REQUEST,
#                     )
#         except errors.ValidationError:
#             return Fortauto.response(
#                 {"message": "error validating payment details"},
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         except Exception.__base__:
#             return Fortauto.response(
#                 {"message": "error updating user credit account"},
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
#     return Fortauto.response(
#         {"message": f"Error validating admin"}, status_code=status.HTTP_401_UNAUTHORIZED
#     )

# @user_deposit.get("/")
# async def get_user_depositd_balance(user: dict = Depends(UserMixin.authenticate_user)):
#     try:
#         user_account = Deposit.get_user_account(userId=user["id"])
#         if user_account:
#             return Fortauto.response(
#                 {"message": user_account.to_json()}, status_code=status.HTTP_201_CREATED
#             )
#         return Fortauto.response(
#             {"message": "User does not have any credit account"},
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )
#     except Exception.__base__:
#         return Fortauto.response(
#             {"message": "error getting user credit account"},
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )

# @user_deposit.delete("/{userId}")
# async def remove_user_deposit_account(
#     user: dict = Depends(UserMixin.authenticate_user),
# ):
#     if user["super_admin"]:
#         try:
#             user_account = Deposit.get_user_account(userId=user["id"])
#             if user_account:
#                 user_account.delete()
#                 return Fortauto.response(
#                     {"message": "user credit account was removed"},
#                     status_code=status.HTTP_200_OK,
#                 )
#             return Fortauto.response(
#                 {"message": "User does not have any credit account"},
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         except Exception.__base__:
#             return Fortauto.response(
#                 {"message": "error removing user credit account"},
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
#     return Fortauto.response(
#         {"message": "error validating admin"}, status_code=status.HTTP_401_UNAUTHORIZED
#     )
