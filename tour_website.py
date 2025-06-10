import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Padharo Maahre Desh - Tour & Travel",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .logo-text {
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .tagline {
        font-size: 1.2rem;
        opacity: 0.9;
        font-style: italic;
    }
    
    .package-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #ff6b35;
    }
    
    .package-title {
        color: #ff6b35;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .price-tag {
        background: linear-gradient(135deg, #ff6b35, #f7931e);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2rem;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .feature-list {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .book-button {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .book-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

if 'selected_package' not in st.session_state:
    st.session_state.selected_package = None

# Tour packages data
packages = {
    "Golden Triangle Heritage": {
        "price": "₹15,999",
        "duration": "5 Days / 4 Nights",
        "destinations": ["Jaipur", "Agra", "Delhi"],
        "highlights": [
            "🏛️ Visit iconic Taj Mahal",
            "🏰 Explore Amber Fort & City Palace",
            "🕌 Discover Red Fort & Qutub Minar",
            "🍽️ Traditional Rajasthani cuisine",
            "🚗 Private AC transportation"
        ],
        "temples": ["Birla Mandir", "Akshardham Temple", "Govind Dev Ji Temple"],
        "image_placeholder": "🏛️ Majestic palaces and monuments"
    },
    
    "Rajasthan Royal Experience": {
        "price": "₹22,999",
        "duration": "7 Days / 6 Nights",
        "destinations": ["Udaipur", "Jodhpur", "Jaisalmer", "Pushkar"],
        "highlights": [
            "🏰 Lake Palace & City of Lakes",
            "🐪 Camel safari in Thar Desert",
            "🏛️ Mehrangarh Fort exploration",
            "🎭 Folk dance performances",
            "🏨 Heritage hotel stays"
        ],
        "temples": ["Brahma Temple", "Dilwara Temples", "Eklingji Temple"],
        "image_placeholder": "🏜️ Desert castles and golden sands"
    },
    
    "Spiritual Gujarat Journey": {
        "price": "₹18,999",
        "duration": "6 Days / 5 Nights",
        "destinations": ["Dwarka", "Somnath", "Ahmedabad", "Vadodara"],
        "highlights": [
            "🙏 Visit sacred Dwarkadheesh Temple",
            "🌊 Somnath Jyotirlinga darshan",
            "🏛️ Akshardham Gandhinagar",
            "🎨 Traditional handicraft shopping",
            "✈️ Comfortable accommodation"
        ],
        "temples": ["Dwarkadheesh Temple", "Somnath Temple", "Akshardham", "Swaminarayan Temple"],
        "image_placeholder": "🕉️ Sacred temples and spiritual vibes"
    },
    
    "Himalayan Adventure": {
        "price": "₹28,999",
        "duration": "8 Days / 7 Nights",
        "destinations": ["Rishikesh", "Haridwar", "Mussoorie", "Dehradun"],
        "highlights": [
            "🏔️ Scenic mountain views",
            "🧘 Yoga and meditation sessions",
            "🌊 River Ganga aarti",
            "🚡 Cable car rides",
            "🥾 Nature trekking"
        ],
        "temples": ["Har Ki Pauri", "Mansa Devi Temple", "Chandi Devi Temple"],
        "image_placeholder": "⛰️ Majestic Himalayas and holy rivers"
    },
    
    "South India Temple Trail": {
        "price": "₹24,999",
        "duration": "9 Days / 8 Nights",
        "destinations": ["Chennai", "Madurai", "Rameswaram", "Kanyakumari"],
        "highlights": [
            "🏛️ Magnificent Dravidian architecture",
            "🌊 Sunrise at southernmost tip",
            "🎭 Classical dance performances",
            "🍛 Authentic South Indian cuisine",
            "🏖️ Beautiful coastal views"
        ],
        "temples": ["Meenakshi Temple", "Ramanathaswamy Temple", "Kanyakumari Temple"],
        "image_placeholder": "🏛️ Ancient temples and coastal beauty"
    }
}

def main():
    # Header with logo
    st.markdown("""
    <div class="main-header">
        <div class="logo-text">🏛️ पधारो म्हारे देश</div>
        <div class="logo-text">PADHARO MAAHRE DESH</div>
        <div class="tagline">Discover the Heart of Incredible India</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div class="sidebar-content">
        <h2>🧭 Navigation</h2>
        <p>Explore our amazing tour packages</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "📦 Tour Packages", "📅 My Bookings", "📞 Contact Us"]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "📦 Tour Packages":
        show_packages()
    elif page == "📅 My Bookings":
        show_bookings()
    elif page == "📞 Contact Us":
        show_contact()

def show_home():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🌟 Welcome to Padharo Maahre Desh!")
        st.markdown("""
        Experience the magic of India with our carefully curated tour packages. 
        From majestic palaces to sacred temples, from desert adventures to mountain retreats, 
        we bring you the best of Indian heritage and culture.
        
        ### Why Choose Us?
        - 🏆 **Expert Guides**: Local experts with deep cultural knowledge
        - 🚗 **Comfortable Travel**: AC transportation and quality accommodation
        - 🎯 **Customized Tours**: Tailored experiences for every traveler
        - 💰 **Best Prices**: Competitive rates with no hidden costs
        - 🛡️ **Safe & Secure**: Fully insured and safety-first approach
        """)
        
        if st.button("🚀 Explore Packages Now", key="explore_btn"):
            st.session_state.selected_tab = "packages"
            st.rerun()
    
    with col2:
        st.markdown("### 🎯 Quick Stats")
        st.metric("Happy Travelers", "50,000+")
        st.metric("Tour Packages", "25+")
        st.metric("Cities Covered", "100+")
        st.metric("Customer Rating", "4.8⭐")
        
        st.markdown("### 📱 Contact Info")
        st.info("""
        📞 **Phone**: +91-9876543210
        📧 **Email**: info@padharomaahredesh.com
        🌐 **Website**: www.padharomaahredesh.com
        """)

def show_packages():
    st.markdown("## 📦 Our Premium Tour Packages")
    st.markdown("Choose from our specially designed packages for an unforgettable experience!")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        price_filter = st.selectbox("Price Range", ["All", "Under ₹20,000", "₹20,000 - ₹30,000", "Above ₹30,000"])
    with col2:
        duration_filter = st.selectbox("Duration", ["All", "3-5 Days", "6-8 Days", "9+ Days"])
    with col3:
        region_filter = st.selectbox("Region", ["All", "North India", "West India", "South India"])
    
    # Display packages
    for package_name, package_info in packages.items():
        st.markdown(f"""
        <div class="package-card">
            <div class="package-title">{package_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📍 Destinations:** {', '.join(package_info['destinations'])}")
            st.markdown(f"**⏰ Duration:** {package_info['duration']}")
            
            st.markdown("**✨ Package Highlights:**")
            for highlight in package_info['highlights']:
                st.markdown(f"- {highlight}")
            
            st.markdown("**🏛️ Temple Visits:**")
            for temple in package_info['temples']:
                st.markdown(f"- 🕉️ {temple}")
        
        with col2:
            st.markdown(f"""
            <div class="price-tag">{package_info['price']}</div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"📸 {package_info['image_placeholder']}")
            
            if st.button(f"📖 Book {package_name}", key=f"book_{package_name}"):
                st.session_state.selected_package = package_name
                show_booking_form(package_name, package_info)
        
        st.markdown("---")

def show_booking_form(package_name, package_info):
    st.markdown(f"## 📝 Book Your Trip: {package_name}")
    
    with st.form(f"booking_form_{package_name}"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            email = st.text_input("Email*", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number*", placeholder="+91-9876543210")
            adults = st.number_input("Number of Adults", min_value=1, max_value=10, value=2)
        
        with col2:
            travel_date = st.date_input("Preferred Travel Date", min_value=datetime.now().date())
            children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
            special_requests = st.text_area("Special Requests", placeholder="Any dietary restrictions, accessibility needs, etc.")
        
        # Calculate total price
        base_price = int(package_info['price'].replace('₹', '').replace(',', ''))
        total_adults = adults
        total_children = children
        children_price = base_price * 0.7 * total_children  # 30% discount for children
        total_price = (base_price * total_adults) + children_price
        
        st.markdown(f"### 💰 Price Breakdown:")
        st.markdown(f"- Adults ({total_adults}): ₹{base_price * total_adults:,}")
        if total_children > 0:
            st.markdown(f"- Children ({total_children}): ₹{children_price:,.0f}")
        st.markdown(f"**Total Amount: ₹{total_price:,.0f}**")
        
        submitted = st.form_submit_button("🎉 Confirm Booking", use_container_width=True)
        
        if submitted:
            if name and email and phone:
                booking = {
                    'package': package_name,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'travel_date': travel_date,
                    'adults': adults,
                    'children': children,
                    'total_price': total_price,
                    'special_requests': special_requests,
                    'booking_date': datetime.now(),
                    'booking_id': f"PMD{datetime.now().strftime('%Y%m%d%H%M%S')}"
                }
                
                st.session_state.bookings.append(booking)
                
                st.success(f"""
                🎉 **Booking Confirmed!**
                
                **Booking ID:** {booking['booking_id']}
                **Package:** {package_name}
                **Total Amount:** ₹{total_price:,.0f}
                
                📧 Confirmation email will be sent to {email}
                📞 Our team will contact you at {phone} within 24 hours
                
                Thank you for choosing Padharo Maahre Desh! 🙏
                """)
                
                st.balloons()
            else:
                st.error("Please fill in all required fields marked with *")

def show_bookings():
    st.markdown("## 📅 My Bookings")
    
    if not st.session_state.bookings:
        st.info("No bookings found. Book your first trip now!")
        if st.button("🚀 Browse Packages"):
            st.session_state.selected_tab = "packages"
            st.rerun()
    else:
        for booking in st.session_state.bookings:
            with st.expander(f"🎫 {booking['booking_id']} - {booking['package']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**👤 Name:** {booking['name']}")
                    st.markdown(f"**📧 Email:** {booking['email']}")
                    st.markdown(f"**📞 Phone:** {booking['phone']}")
                    st.markdown(f"**📅 Travel Date:** {booking['travel_date']}")
                
                with col2:
                    st.markdown(f"**👥 Travelers:** {booking['adults']} Adults, {booking['children']} Children")
                    st.markdown(f"**💰 Total Amount:** ₹{booking['total_price']:,.0f}")
                    st.markdown(f"**📋 Booking Date:** {booking['booking_date'].strftime('%Y-%m-%d %H:%M')}")
                
                if booking['special_requests']:
                    st.markdown(f"**📝 Special Requests:** {booking['special_requests']}")
                
                st.success("✅ Booking Confirmed - Payment Pending")

def show_contact():
    st.markdown("## 📞 Contact Us")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏢 Office Information
        
        **📍 Address:**
        Padharo Maahre Desh Tours & Travels
        123, Heritage Plaza, MI Road
        Jaipur, Rajasthan - 302001
        
        **📞 Phone Numbers:**
        - Main Office: +91-141-2345678
        - Mobile: +91-9876543210
        - WhatsApp: +91-9876543210
        
        **📧 Email:**
        - General Inquiries: info@padharomaahredesh.com
        - Bookings: bookings@padharomaahredesh.com
        - Support: support@padharomaahredesh.com
        
        **🕒 Office Hours:**
        Monday - Saturday: 9:00 AM - 7:00 PM
        Sunday: 10:00 AM - 5:00 PM
        """)
    
    with col2:
        st.markdown("### 💬 Send Us a Message")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            subject = st.selectbox("Subject", [
                "General Inquiry",
                "Package Information", 
                "Booking Support",
                "Complaint/Feedback",
                "Custom Tour Request"
            ])
            message = st.text_area("Your Message", height=150)
            
            if st.form_submit_button("📤 Send Message"):
                if name and email and message:
                    st.success("""
                    ✅ **Message Sent Successfully!**
                    
                    Thank you for contacting us. We'll get back to you within 24 hours.
                    """)
                else:
                    st.error("Please fill in all fields.")
    
    # Map placeholder
    st.markdown("### 🗺️ Find Us")
    st.info("📍 Located in the heart of Jaipur, easily accessible by all modes of transport")

if __name__ == "__main__":
    main()