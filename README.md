# --- HOMEPAGE ---
def show_home():
    st.markdown("<h1 style='color:#ff6b35;'>🏛️ Padharo Maahre Desh</h1>", unsafe_allow_html=True)
    st.subheader("🌏 Explore India like never before!")
    st.markdown("## 🎞️ Featured Tour Packages")
    cols = st.columns(4)
    for idx, (pkg, img) in enumerate(package_images.items()):
        with cols[idx % 4]:
            st.image(img, caption=pkg, use_container_width=True)
            st.markdown(f"**{pkg}**")
            st.markdown(f"💰 {packages[pkg]['price']} | ⏳ {packages[pkg]['duration']}")
            if st.button("📖 View Details", key=f"slider_book_{pkg}"):
                st.session_state.selected_package = pkg
                st.session_state.selected_tab = "📦 Tour Packages"
                st.rerun()

# --- PACKAGE LIST PAGE ---
def show_packages():
    st.title("📦 Tour Packages")
    for pkg, data in packages.items():
        st.subheader(pkg)
        st.image(package_images[pkg], use_container_width=True)
        st.markdown(f"**Price:** {data['price']} | **Duration:** {data['duration']}")
        st.markdown(f"**Destinations:** {', '.join(data['destinations'])}")
        st.markdown("**Highlights:**")
        for h in data['highlights']:
            st.markdown(f"- {h}")
        st.markdown("**Temples:**")
        for t in data['temples']:
            st.markdown(f"- {t}")
        if st.button(f"📝 Book {pkg}", key=f"bookbtn_{pkg}"):
            st.session_state.selected_package = pkg
            show_package_details(pkg)
            return
        st.markdown("---")

# --- PACKAGE DETAIL PAGE ---
def show_package_details(pkg_name):
    data = packages[pkg_name]
    st.header(f"📦 {pkg_name}")
    st.image(package_images[pkg_name], use_container_width=True)
    st.markdown(f"**Price:** {data['price']} | **Duration:** {data['duration']}")
    st.markdown(f"**Destinations:** {', '.join(data['destinations'])}")
    st.markdown("**Highlights:**")
    for h in data['highlights']:
        st.markdown(f"- {h}")
    st.markdown("**Temples Included:**")
    for t in data['temples']:
        st.markdown(f"- {t}")
    if st.button("🚀 Proceed to Booking", key=f"bookform_{pkg_name}"):
        show_booking_form(pkg_name)

# --- BOOKING FORM ---
def show_booking_form(pkg_name):
    data = packages[pkg_name]
    st.subheader(f"📝 Book: {pkg_name}")
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone*")
        with col2:
            date = st.date_input("Travel Date", min_value=datetime.today())
            people = st.number_input("Number of Travelers", 1, 20, 2)
            note = st.text_area("Special Requests (Optional)")
        base = int(data["price"].replace("₹", "").replace(",", ""))
        total = base * people
        st.markdown(f"### 💰 Estimated Total: ₹{total:,}")
        confirm = st.form_submit_button("✅ Confirm Booking")
        if confirm and name and email and phone:
            booking = {
                "package": pkg_name,
                "name": name,
                "email": email,
                "phone": phone,
                "people": people,
                "date": date,
                "note": note,
                "total": total,
                "id": f"PMD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            st.session_state.bookings.append(booking)
            st.success(f"✅ Booking Confirmed! ID: {booking['id']}")
            st.balloons()
        elif confirm:
            st.error("Please fill all required fields.")

# --- BOOKINGS PAGE ---
def show_bookings():
    st.title("📅 My Bookings")
    if not st.session_state.bookings:
        st.info("No bookings yet.")
        return
    for b in st.session_state.bookings:
        with st.expander(f"{b['id']} - {b['package']}"):
            st.markdown(f"- **Name:** {b['name']}")
            st.markdown(f"- **Email:** {b['email']}")
            st.markdown(f"- **Phone:** {b['phone']}")
            st.markdown(f"- **Travel Date:** {b['date']}")
            st.markdown(f"- **Travelers:** {b['people']}")
            st.markdown(f"- **Total:** ₹{b['total']:,}")
            if b['note']:
                st.markdown(f"- **Special Requests:** {b['note']}")

# --- CONTACT US PAGE ---
def show_contact():
    st.title("📞 Contact Us")
    st.markdown("""
📍 **Address**: Heritage Plaza, Jaipur  
📧 **Email**: info@padharomaahredesh.com  
📞 **Phone**: +91-9876543210  
🕒 **Timings**: 9:00 AM – 7:00 PM (Mon–Sat)
    """)
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        msg = st.text_area("Message")
        submit = st.form_submit_button("Send")
        if submit:
            if name and email and msg:
                st.success("✅ Message sent successfully.")
            else:
                st.error("Please fill all fields.")

# --- ROUTER ---
tabs = ["🏠 Home", "📦 Tour Packages", "📅 My Bookings", "📞 Contact Us"]
selected = st.sidebar.selectbox("Choose a section:", tabs, index=tabs.index(st.session_state.selected_tab))
st.session_state.selected_tab = selected

if selected == "🏠 Home":
    show_home()
elif selected == "📦 Tour Packages":
    if st.session_state.selected_package:
        show_package_details(st.session_state.selected_package)
        st.session_state.selected_package = None
    else:
        show_packages()
elif selected == "📅 My Bookings":
    show_bookings()
elif selected == "📞 Contact Us":
    show_contact()
