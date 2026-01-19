# Provider CRUD Operations - Testing Guide

## Overview
This guide covers all CRUD (Create, Read, Update, Delete) operations available for service providers in the HomeServe platform.

## Prerequisites
1. Activate the virtual environment:
   ```powershell
   cd c:\entry\frontend\django_folder\homeserve
   ..\my_virtual\Scripts\Activate.ps1
   ```

2. Start the development server:
   ```powershell
   python manage.py runserver
   ```

3. Have a provider account ready:
   - If you don't have one, create a user account and complete provider onboarding at: `http://127.0.0.1:8000/provider-onboarding/`
   - Or use existing provider credentials (e.g., `provider1` / `password123`)

## Provider Profile CRUD Operations

### ✅ CREATE Provider Profile
**URL:** `http://127.0.0.1:8000/provider-onboarding/`

**Steps:**
1. Register as a new user or login with an existing user account
2. Navigate to provider onboarding
3. Fill in the provider registration form:
   - Business Name (required)
   - Contact Number (required)
   - Email (required)
   - Address (required)
   - City, State, Pincode (required)
   - Years of Experience
   - Bio/Description (required)
   - Profile Image (optional)
4. Submit the form
5. **Expected Result:** Provider profile created, redirected to provider dashboard

### 📖 READ Provider Profile
**URL:** `http://127.0.0.1:8000/provider/profile/`

**Steps:**
1. Login as a provider
2. Navigate to Provider Portal → Profile
3. **Expected Result:** View complete provider profile with all details:
   - Business information
   - Contact details
   - Address
   - Verification status
   - Rating and reviews count
   - Total bookings

### ✏️ UPDATE Provider Profile
**URL:** `http://127.0.0.1:8000/provider/profile/edit/`

**Steps:**
1. Login as a provider
2. Navigate to Provider Portal → Profile → Edit Profile
3. Modify any fields:
   - Business Name
   - Contact Numbers
   - Email
   - Address (full address, city, state, pincode)
   - Experience Years
   - Bio/Description
   - Profile Image
4. Click "Save Changes"
5. **Expected Result:** Success message displayed, redirected to profile page with updated information

### ❌ DELETE Provider Profile
**Note:** Provider profile deletion is not directly available through the UI for data integrity. This should be done through Django admin panel if absolutely necessary.

---

## Service CRUD Operations

### ✅ CREATE Service
**URL:** `http://127.0.0.1:8000/provider/services/add/`

**Steps:**
1. Login as a provider
2. Navigate to Provider Portal → My Services
3. Click "+ Add New Service"
4. Fill in service details:
   - Service Title (required)
   - Category (required - select from dropdown)
   - Description (required)
   - Pricing Type (Fixed Price, Hourly Rate, or Negotiable)
   - Price (required)
   - Duration in Minutes (default: 60)
   - Emergency Service Available (checkbox)
   - Service Image (optional)
5. Click "Add Service"
6. **Expected Result:** 
   - Success message: "Service '[Name]' submitted successfully! Waiting for admin approval."
   - Service appears in "My Services" list with "Pending Approval" status
   - Redirected to services list page

**Test Cases:**
- Add service with all required fields only
- Add service with optional fields (image, emergency availability)
- Try different pricing types
- Test validation (empty fields should show errors)

### 📖 READ Services
**URL:** `http://127.0.0.1:8000/provider/services/`

**Steps:**
1. Login as a provider
2. Navigate to Provider Portal → My Services
3. **Expected Result:** View all services in a grid layout showing:
   - Service title and price
   - Category
   - Description (truncated)
   - Approval status (Pending, Approved, Rejected)
   - Active/Inactive status
   - Average rating and booking count
   - Action buttons (Edit, View Bookings, Delete)

**Dashboard Stats Displayed:**
- Total Services count
- Active Services count
- Total Bookings count
- Average Price

### ✏️ UPDATE Service
**URL:** `http://127.0.0.1:8000/provider/services/edit/<service_id>/`

**Steps:**
1. Login as a provider
2. Navigate to Provider Portal → My Services
3. Find the service you want to edit
4. Click "Edit" button on the service card
5. Modify any fields in the form
6. Click "Update Service"
7. **Expected Result:**
   - Success message: "Service '[Name]' updated successfully!"
   - Changes reflected in service list
   - If service was previously rejected, status changes back to "Pending Approval"
   - Redirected to services list

**Test Cases:**
- Edit service title and description
- Change pricing type and price
- Update service image (replace existing)
- Toggle emergency availability
- Edit a rejected service (should reset to pending)

### ❌ DELETE Service
**URL:** `http://127.0.0.1:8000/provider/services/delete/<service_id>/`

**Steps:**
1. Login as a provider
2. Navigate to Provider Portal → My Services
3. Find the service you want to delete
4. Click "Delete" button (red button)
5. **Confirmation Dialog:** JavaScript confirm popup appears
   - Message: "Are you sure you want to delete '[Service Name]'? This action cannot be undone."
6. Click "OK" to confirm or "Cancel" to abort
7. If confirmed, redirected to confirmation page showing:
   - Service details (title, category, price, description)
   - Warning message
   - "Cancel" and "Yes, Delete Service" buttons
8. Click "Yes, Delete Service" to permanently delete
9. **Expected Result:**
   - Success message: "Service '[Name]' deleted successfully!"
   - Service removed from services list
   - Stats updated (total count decreased)
   - Redirected to services list

**Test Cases:**
- Delete an approved service
- Delete a pending service
- Cancel deletion from JavaScript popup
- Cancel deletion from confirmation page
- Verify service is permanently deleted (check in list)

---

## Complete Testing Workflow

### Scenario 1: New Provider Onboarding
1. ✅ CREATE profile via onboarding
2. 📖 READ profile to verify details
3. ✅ CREATE first service
4. Wait for admin approval (or approve via admin panel)
5. ✏️ UPDATE service details
6. 📖 READ services list to verify changes

### Scenario 2: Service Management
1. ✅ CREATE 3-5 different services in various categories
2. 📖 READ all services in dashboard
3. ✏️ UPDATE one service (change price and description)
4. ❌ DELETE one service
5. Verify remaining services count is correct

### Scenario 3: Profile Updates
1. 📖 READ current profile
2. ✏️ UPDATE business name and contact number
3. ✏️ UPDATE profile image
4. ✏️ UPDATE bio and experience
5. 📖 READ profile to verify all changes

---

## Admin Operations (via Django Admin)

### Approve/Reject Services
**URL:** `http://127.0.0.1:8000/admin/services/service/`

**Steps:**
1. Login as superuser
2. Navigate to Services → Services
3. Click on a service
4. Change "Approval status" from "Pending Approval" to "Approved" or "Rejected"
5. If rejecting, add "Rejection reason"
6. Save
7. **Expected Result:** Provider sees updated status in their dashboard

### Verify Provider
**URL:** `http://127.0.0.1:8000/admin/services/serviceprovider/`

**Steps:**
1. Login as superuser
2. Navigate to Services → Service Providers
3. Click on a provider
4. Change "Verification status" from "Pending Verification" to "Verified"
5. Set "Verified at" to current date/time
6. Save
7. **Expected Result:** Provider profile shows "Verified" badge

---

## API Testing (Optional)

### GET Provider Services (API)
```powershell
curl http://127.0.0.1:8000/api/providers/1/services/
```

### GET Provider Profile (API)
```powershell
curl http://127.0.0.1:8000/api/providers/1/
```

---

## Troubleshooting

### Issue: Can't access provider portal
**Solution:** Ensure user has a provider profile by completing onboarding

### Issue: Service not showing in list
**Solution:** 
- Check if service was created successfully
- Verify approval status in admin panel
- Check if service belongs to the logged-in provider

### Issue: Delete button not working
**Solution:**
- Check browser console for JavaScript errors
- Ensure CSRF token is present in the page
- Try accessing delete URL directly: `/provider/services/delete/<id>/`

### Issue: Images not uploading
**Solution:**
- Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured in settings
- Check file size (max upload size limits)
- Verify media directory has write permissions

---

## Summary of URLs

| Operation | URL | Method |
|-----------|-----|--------|
| Create Profile | `/provider-onboarding/` | POST |
| View Profile | `/provider/profile/` | GET |
| Edit Profile | `/provider/profile/edit/` | GET/POST |
| Change Password | `/provider/profile/change-password/` | GET/POST |
| List Services | `/provider/services/` | GET |
| Create Service | `/provider/services/add/` | GET/POST |
| Edit Service | `/provider/services/edit/<id>/` | GET/POST |
| Delete Service | `/provider/services/delete/<id>/` | GET/POST |

---

## Screenshots Checklist

For comprehensive documentation, capture screenshots of:

1. ✅ **Provider Onboarding Form** (empty state)
2. ✅ **Provider Dashboard** (after creation)
3. ✅ **Provider Profile Page** (read view)
4. ✅ **Edit Profile Form** (with populated data)
5. ✅ **Services List** (empty state)
6. ✅ **Add Service Form** (empty state)
7. ✅ **Services List** (with services)
8. ✅ **Service Card** (showing all buttons)
9. ✅ **Edit Service Form** (populated)
10. ✅ **Delete Confirmation Dialog** (JavaScript popup)
11. ✅ **Delete Confirmation Page** (template)
12. ✅ **Success Messages** (create, update, delete)
13. ✅ **Validation Errors** (empty required fields)
14. ✅ **Approval Status Badges** (pending, approved, rejected)
15. ✅ **Admin Panel** (service approval interface)

---

## Expected Behavior Summary

### ✅ CREATE Operations
- Forms validate required fields
- Success messages displayed
- Redirects to appropriate page
- Data persisted in database

### 📖 READ Operations
- All data displayed correctly
- Stats calculated accurately
- Filtering/sorting works (if applicable)
- Images load properly

### ✏️ UPDATE Operations
- Form pre-filled with current data
- Changes saved successfully
- Success feedback provided
- No data loss on errors

### ❌ DELETE Operations
- Confirmation required (two-step process)
- Success message after deletion
- Data actually removed from database
- Related data handled properly (bookings remain but service removed)

---

## Notes

1. **Security:** All provider operations require authentication and provider profile verification
2. **Authorization:** Providers can only manage their own services
3. **Data Integrity:** Deleting services doesn't affect past bookings (referential integrity)
4. **Approval Workflow:** New services require admin approval before becoming visible to customers
5. **Image Handling:** Profile and service images stored in media directory
6. **Validation:** Both client-side and server-side validation in place

---

## Next Steps

After completing CRUD operations testing:
1. Test booking management features
2. Test earnings and analytics dashboard
3. Test messaging system
4. Test calendar and availability management
5. Test review responses

---

**Last Updated:** January 19, 2026
**Django Version:** 4.x
**Project:** HomeServe - Home Services Marketplace
