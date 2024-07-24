import streamlit as st
from streamlit_option_menu import option_menu

@st.cache_data
def load_data(url) :
    df = pd.read_csv(url)
    return df

st.markdown("""
    <header>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
    </header>
    <style>
        html, body, h1, h2, h3, p, b, nav-link [class*="css"] {font-family: 'Poppins', sans-serif;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar :
    selected = option_menu('Monte Carlo',
                           ['1.', '2.', '3.', '4.', '5.', '6.'],
                           icons = ["person-circle", "person-workspace", "person-badge-fill", "person-circle", "person-workspace", "person-badge-fill"],
                           menu_icon = "person-lines-fill",
                           default_index = 0,
                           styles={"nav" : {"font-family" : 'Poppins'},
                                   "menu-title" : {"font-family" : 'Poppins', "font-weight" : "700"},
                                   "nav-link-selected" : {"font-weight" : "700", "background-color" : "#dc3545"},
                                   "icon" : {"font-size" : "20px"},
                                   "nav-link" : {"--hover-color" : "#dc3545"}})
    
if (selected == '1.') :
    st.header(f"1.")
    
if (selected == '2.') :
    st.header(f"2.")
    
if (selected == '3.') :
    st.header(f"3.")
    
if (selected == '4.') :
    st.header(f"4.")
    
if (selected == '5.') :
    st.header(f"5.")
    
if (selected == '6.') :
    st.header(f"6.")
    
