import streamlit as st
import mysql.connector
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import time

st.set_option('deprecation.showfileUploaderEncoding', False)

from userfn import login, signup, get_details, place_order, update_details, update_password, delete_user, get_order_info


st.set_page_config(page_title='Order Food Now !', page_icon=None,
                   layout="centered", initial_sidebar_state="auto", menu_items=None)

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
checkoutSection = st.container()

food_list = [None, None, None]
qty_list = [None, None, None]
amt_list = [None, None, None]

order = {
    'Food Name': food_list,
    'Qty': qty_list,
    'Amount': amt_list
}


# Custom HTML and CSS to change the outline color
# custom_style = """
#     <style>
#         input:focus {
#             border-color: #00ff00;  /* Change the color to your desired outline color */
#             box-shadow: 0 0 5px #00ff00;  /* Add a box shadow if desired */
#         }
#     </style>
# """

# # Display the custom style
# st.markdown(custom_style, unsafe_allow_html=True)


cart = pd.DataFrame(order)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database="ofds"
)

mc = db.cursor()


def order_pressed(total_amt, paymentmethod, food_list, qty_list):
    if place_order(total_amt, paymentmethod, food_list, qty_list):
        st.session_state['checkout'] = True
        st.session_state['loggedIn'] = False


def show_checkout_page():
    with checkoutSection:
        if st.session_state['checkout'] == True:

            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            st.success(
                f"Hey {st.session_state['details'][1]}, Your Order has been placed Successfully!")
            st.balloons()
            st.subheader(
                f"Your order will arrive to your address : {st.session_state['details'][4]} .")
            st.subheader(
                f"Our rider will contact you at : {st.session_state['details'][2]}")

        if st.button("Back to Main Page") and st.session_state['checkout']:
            st.session_state['loggedIn'] = True
            st.session_state['checkout'] = False


def update_user_details(user_id, email, name, address, number):
    if update_details(user_id, email, name, address, number):
        st.info("User Information Updated Successfully, you will need to login again.")
        LoggedOut_Clicked()
    else:
        st.info("Error Detected while updating")


def update_user_password(user_id, password):
    if update_password(user_id, password):
        st.info("Password updated successfully, you will be logged out now")
        LoggedOut_Clicked()
    else:
        st.info("Eroor Detected while updating password")


def show_main_page():
    with mainSection:
        st.header(f" Welcome, {st.session_state['details'][1]} !")

        pizzaplace, noodleplace, burgerplace, cart, orders, myaccount = st.tabs(
            ['Pizza Place', 'Noodle Place', 'Burger Place', 'Cart', 'Orders', 'My Account'])

        with pizzaplace:
            col1 = st.columns(1)
            col1[0].image('pizza.jpg', caption="Pizza 🍕")
            # col1.text("Pizza 🍕")
            if col1[0].checkbox(label='Order Pizza @ ₹199', key=9):
                col1[0].text('Enter QTY. -')
                c_pizza = col1[0].number_input(label="", min_value=1, key=79)
                food_list[0] = 'pizza'
                qty_list[0] = int(c_pizza)
                amt_list[0] = int(c_pizza) * 199

        with burgerplace:
            col2 = st.columns(1)
            col2[0].image('burger.jpg')
            col2[0].text("Burger 🍔")
            if col2[0].checkbox('Order Burger @ ₹99', key=69):
                col2[0].text('Enter QTY. -')
                c_burger = col2[0].number_input(label="", min_value=1, key=89)

                food_list[1] = 'burger'
                qty_list[1] = int(c_burger)
                amt_list[1] = int(c_burger) * 99

        with noodleplace:
            col3 = st.columns(1)
            col3[0].image('noodles.jpg')
            col3[0].text("Noodles 🍜")
            if col3[0].checkbox('Order noodles @ ₹149', key=19):
                col3[0].text('Enter QTY. -')
                c_noodles = col3[0].number_input(
                    label="", min_value=1, key=129)
                food_list[2] = 'noodles'
                qty_list[2] = int(c_noodles)
                amt_list[2] = int(c_noodles) * 149

        # with menu:

        #     st.subheader(
        #         'Please Select the Food and quantity that you want to order')

        #     col1, col2, col3 = st.columns(3)
        #     col1.image('pizza.jpg')
        #     col1.text("Pizza 🍕")
        #     if col1.checkbox(label='Order Pizza @ ₹199', key=1):
        #         col1.text('Enter QTY. -')
        #         c_pizza = col1.number_input(label="", min_value=1, key=79)
        #         food_list[0] = 'pizza'
        #         qty_list[0] = int(c_pizza)
        #         amt_list[0] = int(c_pizza) * 199

        #     col2.image('burger.jpg')
        #     col2.text("Burger 🍔")
        #     if col2.checkbox('Order Buger @ ₹99', key=2):
        #         col2.text('Enter QTY. -')
        #         c_burger = col2.number_input(label="", min_value=1, key=89)

        #         food_list[1] = 'burger'
        #         qty_list[1] = int(c_burger)
        #         amt_list[1] = int(c_burger) * 99

        #     col3.image('noodles.jpg')
        #     col3.text("Noodles 🍜")
        #     if col3.checkbox('Order noodles @ ₹149', key=3):
        #         col3.text('Enter QTY. -')
        #         c_noodles = col3.number_input(label="", min_value=1, key=69)
        #         food_list[2] = 'noodles'
        #         qty_list[2] = int(c_noodles)
        #         amt_list[2] = int(c_noodles) * 149

            with cart:
                hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                 """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)

                order = {
                    'Food Name': food_list,
                    'Qty': qty_list,
                    'Amount': amt_list
                }

                cart = pd.DataFrame(order)
                cart_final = cart.dropna()
                cart_final['Qty'].astype(int)
                st.table(cart_final)
                total_amt = [amt for amt in amt_list if amt != None]
                total_item = [food for food in food_list if food != None]
                total_qty = [qty for qty in qty_list if qty != None]
                total_sum = sum(total_amt)
                st.subheader("Your Total Amout to be paid" +
                             ': ₹' + str(float(total_sum)))

                payment = st.selectbox(
                    'How would you like to Pay', ('Cash/Pay on delivery', 'UPI', 'Net Banking', 'Credit Card', 'Debit Card'))

                st.button("Order Now", on_click=order_pressed, args=(
                    total_sum, payment, total_item, total_qty))

            with myaccount:
                # st.write(st.session_state['details'])r
                st.header('Update your details here')
                st.subheader("Enter updated email")
                up_email = st.text_input(label="", value=str(
                    st.session_state['details'][3]), key=12345)
                st.subheader("Enter updated name")
                up_name = st.text_input(label="", value=str(
                    st.session_state['details'][1]), key=1234567)
                st.subheader("Enter updated address")
                up_address = st.text_input(
                    label="", value=str(st.session_state['details'][4]), key=8975)
                st.subheader("Enter updated phone number")
                up_number = st.text_input(
                    label="", value=str(st.session_state['details'][2]), key=1239886)

                st.button('Update User Details', on_click=update_user_details, args=(
                    st.session_state['details'][0], up_email, up_name, up_address, up_number))

                if st.checkbox("Do you want to change the password ?"):
                    st.subheader('Write Updated Password :')
                    up_passw = st.text_input(
                        label="", value="", placeholder="Enter updated password", type="password", key=2568)
                    up_conf_passw = st.text_input(
                        label="", value="", placeholder="Enter updated password", type="password", key=2576)
                    if up_passw == up_conf_passw:
                        st.button('Update Password', on_click=update_user_password, args=(
                            st.session_state['details'][0], up_passw))
                    else:
                        st.info('Password does not match ')

                if st.checkbox("Do you want to Delete your account ? "):
                    st.subheader(
                        "Are you sure you want to delete your account ?")
                    # st.text(st.session_state['details'][0])
                    st.button('DELETE MY ACCOUNT', on_click=delete_user_show, args=(
                        st.session_state['details'][0],))
            with orders:

                if st.checkbox("View order details: "):

                    order_info = get_order_info()
                    columns = ['Order ID', 'Restaurant Name',
                               'Payment Method', 'Order Total', 'Name', 'Address', 'Phone']
                    order_df = pd.DataFrame(order_info, columns=columns)

                    st.title('Order Information')
                    # Display order information as a table
                    st.table(order_df)


def delete_user_show(urd_id):
    delete_user(urd_id)
    LoggedOut_Clicked()
    st.success("Account Deleted Successfuly")


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['details'] = None
    st.session_state['checkout'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedIn_Clicked(email_id, password):
    if login(email_id, password):
        st.session_state['loggedIn'] = True
        st.session_state['details'] = get_details(email_id)
    else:
        st.session_state['loggedIn'] = False
        st.session_state['details'] = None
        st.error("Invalid user name or password")


def signup_clicked(name, email, address, phnumber, sign_password):
    try:
        if signup(email, name, address, phnumber, sign_password):
            st.success("Successfully signed up")
            st.balloons()
    except:
        st.warning('Invalid User ID or user ID already taken')


def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:

            login, signup = st.tabs(["Login ", "Sign Up"])
            with login:
                st.subheader('Login Here ')
                email_id = st.text_input(
                    label="Email", value="", placeholder="", help="Enter your registered email address")
                password = st.text_input(
                    label="Password", value="", placeholder="", type="password", help="Enter your password")
                st.button("Login", on_click=LoggedIn_Clicked,
                          args=(email_id, password))
            with signup:
                st.subheader('Sign Up')
                email = st.text_input(
                    label="", value="", placeholder="Enter your Email-ID", key=106)
                name = st.text_input(label="", value="",
                                     placeholder="Enter your Name", key=100)

                address = st.text_input(
                    label="", value="", placeholder="Enter your Address:", key=13)

                phnumber = st.text_input(
                    label="", value="+91 ", placeholder='Enter you Phone Number', key=14)

                sign_password = st.text_input(
                    label="", value="", placeholder="Enter password", type="password", key=1100)
                cnf_password = st.text_input(
                    label="", value="", placeholder="confirm your password", type="password", key=12)
                st.button("Sign up", on_click=signup_clicked, args=(
                    email, name, address, phnumber, sign_password))
                if sign_password != cnf_password:
                    st.warning('Password does not match')


with headerSection:
    st.title("Online Food Ordering System ")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    if 'checkout' not in st.session_state:
        st.session_state['checkout'] = False
    else:
        if st.session_state['loggedIn']:
            show_logout_page()
            show_main_page()
        elif st.session_state['checkout']:
            show_logout_page()
            show_checkout_page()
        else:
            show_login_page()


hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
              input:focus {
            border-color: #00ff00;  
            box-shadow: 0 0 5px #00ff00; 
        }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
