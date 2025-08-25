import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import json





if st.session_state.page == "welcome":
    if os.path.exists("welcome.jpg"):
        st.image("welcome.jpg", use_column_width=True)
    if st.button("____________👉 Click to Continue____________", key="start"):
        st.session_state.page = "menu"
        st.rerun()

elif st.session_state.page == "menu":
    st.title("📋 What would you like to do?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 Big Vocabulary", key="start_vocabulary"):
            st.session_state.page = "Vocabulary"
            st.session_state_index = 0
            st.rerun()
    with col2:
        if st.button("📋 Simple, Easy and Cozy Grammer", key="grammer"):
            st.session_state.page = "grammer"
            st.session_state.order_index = 0
            st.rerun()
    with col3:
        if st.button("👩🏼‍💼Talk with Aqiiii", key = "talk"):
           st.session_state.page = "talk"
           st.session_state.order_index = 0
           st.rerun()
  

elif st.session_state.page == "New Stock":
    st.header("🛒 New Order - Add Items to Order List")

    if "order_data" not in st.session_state:
        st.session_state.order_data = {}
    if "order_index" not in st.session_state:
        st.session_state.order_index = 0

    if st.session_state.order_index < len(inventory_items):
        item = inventory_items[st.session_state.order_index]
        st.subheader(f"Item {st.session_state.order_index + 1} of {len(inventory_items)}: {item['name']}")

        image_path = item['image']
        if item['image'] and os.path.exists(image_path):
            st.image(image_path, width=250)
        else:
            st.warning("📷 Image not found.")

        # Show current order quantity if exists
        current_qty = st.session_state.order_data.get(item['name'], "")

        qty = st.text_input(
            "Enter quantity to order (leave empty to skip):", 
            value=current_qty,
            key=f"order_qty_{st.session_state.order_index}"
        )

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("Next", key=f"order_next_{st.session_state.order_index}"):
                if qty.strip():  # Only add to order if quantity is provided
                    st.session_state.order_data[item['name']] = qty
                st.session_state.order_index += 1
                save_order_progress()
                st.rerun()

        with col2:
            if st.button("Back", key=f"order_back_{st.session_state.order_index}"):
                if st.session_state.order_index > 0:
                    st.session_state.order_index -= 1
                    save_order_progress()
                    st.rerun()

        with col3:
            if st.button("Skip Item", key=f"order_skip_{st.session_state.order_index}"):
                st.session_state.order_index += 1
                save_order_progress()
                st.rerun()

        with col4:
            if st.button("🗑️ Clear Order", key=f"order_clear_{st.session_state.order_index}"):
                clear_order_progress()
                st.success("✅ Order data cleared!")
                st.rerun()

        with col5:
            if st.button("🏡 Main Menu", key=f"order_menu_{st.session_state.order_index}"):
                st.session_state.page = "menu"
                st.rerun()

        # Show progress
        progress = (st.session_state.order_index / len(inventory_items)) * 100
        st.progress(progress / 100)
        st.write(f"Progress: {st.session_state.order_index}/{len(inventory_items)} items ({progress:.1f}%)")

    else:
        # Show final order summary
        st.success("🎉 Order list complete!")
        st.header("📋 Your Order Summary")

        if st.session_state.order_data:
            total_items = 0
            for item_name, quantity in st.session_state.order_data.items():
                st.write(f"**{item_name}**: {quantity}")
                try:
                    total_items += int(quantity) if quantity.isdigit() else 0
                except:
                    pass

            st.info(f"**Total items to order: {total_items}**")

            def generate_order_pdf(order_dict):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="New Stock Order List", ln=True, align='C')
                pdf.ln(10)

                total = 0
                for item, qty in order_dict.items():
                    pdf.cell(200, 10, txt=f"{item}: {qty}", ln=True)
                    try:
                        total += int(qty) if qty.isdigit() else 0
                    except:
                        pass

                pdf.ln(10)
                pdf.cell(200, 10, txt=f"Total Items: {total}", ln=True)
                return pdf.output(dest="S").encode("latin-1")

            pdf_bytes = generate_order_pdf(st.session_state.order_data)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.download_button(
                    label="📄 Download Order List as PDF",
                    data=pdf_bytes,
                    file_name="New_Stock_Order.pdf",
                    mime="application/pdf"
                )

            with col2:
                if st.button("🔁 Create New Order"):
                    clear_order_progress()
                    st.rerun()

            with col3:
                if st.button("🗑️ Reset Order Data"):
                    clear_order_progress()
                    st.success("✅ Order data cleared!")
                    st.rerun()

            with col4:
                if st.button("🏡 Back to Menu"):
                    st.session_state.page = "menu"
                    st.rerun()

        else:
            st.warning("No items were added to the order.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏡 Back to Menu"):
                    st.session_state.page = "menu"
                    st.rerun()
            with col2:
                if st.button("🗑️ Reset Order Data"):
                    clear_order_progress()
                    st.success("✅ Order data cleared!")
                    st.rerun()

elif st.session_state.page == "inventory":

    # Phase 1: Kitchen Inventory
    if st.session_state.phase == "kitchen":
        st.header("🍳 Step 1: Enter Kitchen Inventory")
        kitchen_items = kitchen_inventory_items

        # Debug info to see what's happening
        st.write(f"Debug: Current index: {st.session_state.index}, Total kitchen items: {len(kitchen_items)}")

        if st.session_state.index < len(kitchen_items):
            item = kitchen_items[st.session_state.index]
            st.subheader(f"Item {st.session_state.index + 1} of {len(kitchen_items)}: {item['name']}")

            image_path = item['image']
            if item['image'] and os.path.exists(image_path):
                st.image(image_path, width=250)
            else:
                st.warning("📷 Image not found.")

            qty = st.text_input(
                "Enter quantity:", 
                value=st.session_state.kitchen_data.get(item['name'], ""), 
                key=f"kitchen_qty_{st.session_state.index}"
            )

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Save & Next", key=f"kitchen_next_{st.session_state.index}"):
                    st.session_state.kitchen_data[item['name']] = qty
                    st.session_state.index += 1
                    save_inventory_progress()
                    st.rerun()
            with col2:
                if st.button("Back", key=f"kitchen_back_{st.session_state.index}"):
                    if st.session_state.index > 0:
                        st.session_state.index -= 1
                        save_inventory_progress()
                        st.rerun()
            with col3:
                if st.button("🗑️ Reset All", key=f"kitchen_reset_{st.session_state.index}"):
                    if os.path.exists(INVENTORY_SAVE_FILE):
                        os.remove(INVENTORY_SAVE_FILE)
                    # Reset all session state properly
                    st.session_state.page = "menu"
                    st.session_state.phase = "kitchen"
                    st.session_state.index = 0
                    st.session_state.kitchen_data = {}
                    st.session_state.store_data = {}
                    st.success("✅ All inventory data cleared!")
                    st.rerun()
            with col4:
                if st.button("🏡 Main Menu", key=f"kitchen_menu_{st.session_state.index}"):
                    st.session_state.page = "menu"
                    save_inventory_progress()
                    st.rerun()
        else:
            st.success("✅ Kitchen inventory complete.")
            if st.button("👉 Continue to Store Inventory", key="continue_to_store"):
                st.session_state.phase = "store"
                st.session_state.index = 0
                save_inventory_progress()
                st.rerun()

    elif st.session_state.phase == "store":
        st.header("🏬 Step 2: Complete Store Inventory")
        if st.session_state.index < len(inventory_items):
            item = inventory_items[st.session_state.index]
            name = item['name']
            st.subheader(f"Item {st.session_state.index + 1} of {len(inventory_items)}: {name}")

            image_path = item['image']
            if item['image'] and os.path.exists(image_path):
                st.image(image_path, width=250)
            else:
                st.warning("📷 Image not found.")

            prev_kitchen = st.session_state.kitchen_data.get(name)
            if prev_kitchen:
                st.info(f"Kitchen quantity previously entered: {prev_kitchen}")

            qty = st.text_input(
                "Enter final store quantity:", 
                value=st.session_state.store_data.get(name, ""), 
                key=f"store_qty_{st.session_state.index}"
            )

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Next", key=f"store_next_{st.session_state.index}"):
                    st.session_state.store_data[name] = qty
                    st.session_state.index += 1
                    save_inventory_progress()
                    st.rerun()
            with col2:
                if st.button("Back", key=f"store_back_{st.session_state.index}"):
                    if st.session_state.index > 0:
                        st.session_state.index -= 1
                        save_inventory_progress()
                        st.rerun()
            with col3:
                if st.button("🗑️ Reset All", key=f"store_reset_{st.session_state.index}"):
                    if os.path.exists(INVENTORY_SAVE_FILE):
                        os.remove(INVENTORY_SAVE_FILE)
                    # Reset all session state properly and go back to main menu
                    st.session_state.page = "menu"
                    st.session_state.phase = "kitchen"
                    st.session_state.index = 0
                    st.session_state.kitchen_data = {}
                    st.session_state.store_data = {}
                    st.success("✅ All inventory data cleared!")
                    st.rerun()
            with col4:
                if st.button("🏡 Main Menu", key=f"store_menu_{st.session_state.index}"):
                    st.session_state.page = "menu"
                    save_inventory_progress()
                    st.rerun()
        else:
            st.success("🎉 All inventory completed. Showing final result...")
            st.session_state.phase = "done"
            save_inventory_progress()
            st.rerun()

    elif st.session_state.phase == "done":
        st.header("📦 Final Store Inventory")
        final_result = st.session_state.store_data
        for name, value in final_result.items():
            st.write(f"**{name}**: {value}")

        def generate_pdf(data_dict):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Final Store Inventory", ln=True, align='C')
            pdf.ln(10)
            for item, val in data_dict.items():
                pdf.cell(200, 10, txt=f"{item}: {val}", ln=True)
            return pdf.output(dest="S").encode("latin-1")

        pdf_bytes = generate_pdf(final_result)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.download_button(
                label="📄 Download Inventory as PDF",
                data=pdf_bytes,
                file_name="Store_Inventory.pdf",
                mime="application/pdf"
            ):
                if os.path.exists(INVENTORY_SAVE_FILE):
                    os.remove(INVENTORY_SAVE_FILE)

        with col2:
            if st.button("🔁 Restart Inventory"):
                if os.path.exists(INVENTORY_SAVE_FILE):
                    os.remove(INVENTORY_SAVE_FILE)
                for key in ["phase", "kitchen_data", "store_data", "index"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        with col3:
            if st.button("🗑️ Reset All Data"):
                if os.path.exists(INVENTORY_SAVE_FILE):
                    os.remove(INVENTORY_SAVE_FILE)
                # Reset all session state properly and go back to main menu
                st.session_state.page = "menu"
                st.session_state.phase = "kitchen"
                st.session_state.index = 0
                st.session_state.kitchen_data = {}
                st.session_state.store_data = {}
                st.rerun()
