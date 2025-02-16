from app.db.session import DBSync
from app.db.models import Permission, Role, Tenant, Outlet
from datetime import datetime

def seed_permissions_and_roles():
    db= DBSync()
    session = db.get_new_session()

    if not session.query(Tenant).filter_by(id=1).first():
        session.add(Tenant(
            id=1,
            name='Restosol HQ',
            contact_name='John Doe',
            contact_email='john.doe@restosol.com',
            contact_phone='+1234567890',
            billing_address='123 Main St, NY, USA',
            subscription_plan='ENTERPRISE',
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ))

    # Seed Outlets
    outlets = [
        (1, 1, 'Restosol Main Outlet', '456 Food Lane', 'New York', 'NY', '10001', 'USA', '+1234567891', '9 AM - 9 PM'),
        (2, 1, 'Restosol Express', '789 Quick St', 'Brooklyn', 'NY', '11201', 'USA', '+1234567892', '10 AM - 8 PM')
    ]

    for outlet_id, tenant_id, name, address, city, state, postal_code, country, phone, hours in outlets:
        if not session.query(Outlet).filter_by(id=outlet_id).first():
            session.add(Outlet(
                id=outlet_id,
                tenant_id=tenant_id,
                name=name,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                phone=phone,
                operating_hours=hours,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))


    permissions = [
        (1, 'create_user', 'User Management', 'Create new users and assign roles'),
        (2, 'update_user', 'User Management', 'Modify existing user details'),
        (3, 'disable_user', 'User Management', 'Deactivate a user account'),
        (4, 'manage_roles', 'Access Control', 'Assign and update user roles'),
        (5, 'multi_location_access', 'Access Control', 'Access multiple business locations'),
        (6, 'process_payment', 'Sales & Transactions', 'Accept and process payments'),
        (7, 'refund_payment', 'Sales & Transactions', 'Handle customer refunds'),
        (8, 'generate_invoice', 'Sales & Transactions', 'Create invoices for sales'),
        (9, 'add_inventory', 'Inventory Management', 'Add and manage stock levels'),
        (10, 'edit_inventory', 'Inventory Management', 'Modify inventory details'),
        (11, 'track_inventory', 'Inventory Management', 'Monitor stock usage and levels'),
        (12, 'manage_services', 'Service Management', 'Create and update service offerings'),
        (13, 'manage_bookings', 'Bookings & Reservations', 'Handle customer bookings and reservations'),
        (14, 'view_reports', 'Reporting & Analytics', 'Access sales and performance reports'),
        (15, 'create_promotions', 'Marketing & Promotions', 'Create and manage discounts and offers'),
        (16, 'view_audit_logs', 'Audit & Logs', 'Track user and system activity logs'),
    ]

    roles = [
        (1, 1, 'owner', 'Full control over the business, settings, users, and reports'),
        (2, 1, 'manager', 'Manages operations, employees, and inventory at one or multiple locations'),
        (3, 1, 'cashier', 'Handles sales, refunds, and billing at a specific location'),
        (4, 1, 'staff', 'Performs day-to-day tasks like serving, assisting, or styling'),
        (5, 1, 'supplier', 'Manages inventory supply, purchase orders, and vendor relationships'),
        (6, 1, 'customer', 'End-user who books services or makes purchases'),
    ]

    # Insert Permissions
    for perm_id, name, category, desc in permissions:
        if not session.query(Permission).filter_by(id=perm_id).first():
            session.add(Permission(id=perm_id, name=name, category=category, description=desc))

    # Insert Roles
    for role_id, tenant_id, name, desc in roles:
        if not session.query(Role).filter_by(id=role_id).first():
            session.add(Role(id=role_id, tenant_id=tenant_id, name=name, description=desc))

    session.commit()
    db.close_session(session)
