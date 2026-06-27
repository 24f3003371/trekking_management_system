import { defineStore } from 'pinia';

export const useTrekStore = defineStore('trek', {
  state: () => {
    // Load from localStorage or set defaults
    const localData = localStorage.getItem('trekflow_state');
    if (localData) {
      try {
        return JSON.parse(localData);
      } catch (e) {
        console.error("Failed to parse local storage state", e);
      }
    }

    return {
      currentUser: null, // logged in user object
      users: [
        { id: 'U001', name: 'Amit Sharma', email: 'user@trekflow.com', password: 'user123', contact: '9876543210', role: 'trekker', status: 'Active' },
        { id: 'U002', name: 'Priya Patel', email: 'priya@gmail.com', password: 'user123', contact: '9123456786', role: 'trekker', status: 'Active' },
        { id: 'U003', name: 'Rahul Verma', email: 'rahul@gmail.com', password: 'user123', contact: '9908776655', role: 'trekker', status: 'Blocked' },
        { id: 'U004', name: 'Sneha Iyer', email: 'sneha@gmail.com', password: 'user123', contact: '9122598765', role: 'trekker', status: 'Active' },
        { id: 'U005', name: 'Karan Tiwari', email: 'karan@gmail.com', password: 'user123', contact: '9871234567', role: 'trekker', status: 'Active' }
      ],
      staff: [
        { id: 'TS01', name: 'Vikram Singh', email: 'staff@trekflow.com', password: 'staff123', contact: '9876543210', role: 'staff', status: 'Active', experience: 5, specialization: 'High Altitude, Wilderness First Aid' },
        { id: 'TS02', name: 'Neha Joshi', email: 'neha@gmail.com', password: 'staff123', contact: '9122598765', role: 'staff', status: 'Blocked', experience: 3, specialization: 'First Aid, Basecamp Management' },
        { id: 'TS03', name: 'Arjun Mehta', email: 'arjun@gmail.com', password: 'staff123', contact: '9908776655', role: 'staff', status: 'Active', experience: 6, specialization: 'Ice Climbing, Navigation' },
        { id: 'TS04', name: 'Pooja Rawat', email: 'pooja@gmail.com', password: 'staff123', contact: '9123454376', role: 'staff', status: 'Active', experience: 4, specialization: 'Flora & Fauna, Trek Leader' },
        { id: 'TS05', name: 'Rohan Kim', email: 'rohan@gmail.com', password: 'staff123', contact: '9871222234', role: 'staff', status: 'Blocked', experience: 2, specialization: 'Photography, Trek Guide' }
      ],
      admin: {
        id: 'A001',
        name: 'Admin User',
        email: 'admin@trekflow.com',
        password: 'admin123',
        role: 'admin'
      },
      treks: [
        { 
          id: 'T001', 
          name: 'Everest Base Camp', 
          location: 'Nepal', 
          difficulty: 'Hard', 
          duration: '12 Days',
          startDate: '2026-05-10',
          endDate: '2026-05-22',
          slots: 15, 
          availableSlots: 8,
          price: 25000, 
          status: 'Open',
          assignedStaffId: 'TS01',
          description: 'The legendary trek to the base of the world\'s highest peak. Experience Sherpa culture and stunning Himalayan panoramas.',
          progress: 0,
          checkpoints: [
            { name: 'Lukla', elevation: '9,380 ft' },
            { name: 'Namche Bazaar', elevation: '11,286 ft' },
            { name: 'Tengboche', elevation: '12,687 ft' },
            { name: 'Dingboche', elevation: '14,468 ft' },
            { name: 'Gorakshep', elevation: '16,942 ft' },
            { name: 'Everest Base Camp', elevation: '17,598 ft' }
          ]
        },
        { 
          id: 'T002', 
          name: 'Roopkund Trek', 
          location: 'Uttarakhand', 
          difficulty: 'Hard', 
          duration: '7 Days',
          startDate: '2026-06-11',
          endDate: '2026-06-18',
          slots: 15, 
          availableSlots: 7,
          price: 18500, 
          status: 'Open',
          assignedStaffId: 'TS01',
          description: 'A high altitude trek in Uttarakhand famous for the mysterious skeleton lake and breathtaking alpine meadows (Bugyals).',
          progress: 20,
          checkpoints: [
            { name: 'Lohajung', elevation: '7,660 ft' },
            { name: 'Didna Camp', elevation: '8,040 ft' },
            { name: 'Ali Bugyal', elevation: '11,000 ft' },
            { name: 'Patari Nachauni', elevation: '12,810 ft' },
            { name: 'Bhagwabasa', elevation: '14,117 ft' },
            { name: 'Roopkund Lake', elevation: '15,750 ft' }
          ]
        },
        { 
          id: 'T003', 
          name: 'Hampta Pass', 
          location: 'Himachal Pradesh', 
          difficulty: 'Moderate', 
          duration: '5 Days',
          startDate: '2026-06-10',
          endDate: '2026-06-14',
          slots: 12, 
          availableSlots: 8,
          price: 15000, 
          status: 'Open',
          assignedStaffId: 'TS03',
          description: 'Contrast trekking at its best. From the lush green valleys of Kullu to the stark desert landscapes of Lahaul and Spiti.',
          progress: 50,
          checkpoints: [
            { name: 'Jobra', elevation: '9,800 ft' },
            { name: 'Jwara', elevation: '11,000 ft' },
            { name: 'Balu Ka Ghera', elevation: '11,900 ft' },
            { name: 'Hampta Pass Crossing', elevation: '14,100 ft' },
            { name: 'Shea Goru', elevation: '12,900 ft' },
            { name: 'Chhatru', elevation: '11,000 ft' }
          ]
        },
        { 
          id: 'T004', 
          name: 'Kedarkantha Trek', 
          location: 'Uttarakhand', 
          difficulty: 'Easy', 
          duration: '4 Days',
          startDate: '2026-05-10',
          endDate: '2026-05-14',
          slots: 20, 
          availableSlots: 15,
          price: 12500, 
          status: 'Open',
          assignedStaffId: 'TS01',
          description: 'A popular winter trek known for its beautiful snowy forest trails, lovely pine glades, and a stunning 360-degree view from the summit.',
          progress: 25,
          checkpoints: [
            { name: 'Base Camp', elevation: '4,200 ft' },
            { name: 'Camp 1', elevation: '6,000 ft' },
            { name: 'Camp 2', elevation: '8,500 ft' },
            { name: 'Camp 3', elevation: '11,000 ft' },
            { name: 'Summit', elevation: '12,500 ft' }
          ]
        },
        { 
          id: 'T005', 
          name: 'Valley of Flowers', 
          location: 'Uttarakhand', 
          difficulty: 'Moderate', 
          duration: '5 Days',
          startDate: '2026-07-05',
          endDate: '2026-07-10',
          slots: 15, 
          availableSlots: 10,
          price: 15000, 
          status: 'Open',
          assignedStaffId: 'TS04',
          description: 'A UNESCO World Heritage site known for its meadows of endemic alpine flowers and outstanding natural beauty in the Western Himalayas.',
          progress: 0,
          checkpoints: [
            { name: 'Govindghat', elevation: '6,300 ft' },
            { name: 'Ghangaria Base', elevation: '9,800 ft' },
            { name: 'Valley Flow Point', elevation: '11,500 ft' },
            { name: 'Hemkund Sahib', elevation: '14,300 ft' }
          ]
        }
      ],
      bookings: [
        { id: 'B001', userId: 'U001', userName: 'Amit Sharma', email: 'user@trekflow.com', trekId: 'T001', trekName: 'Everest Base Camp', bookingDate: '2026-05-12', trekDates: '10 May - 22 May 2026', status: 'Booked' },
        { id: 'B002', userId: 'U002', userName: 'Priya Patel', email: 'priya@gmail.com', trekId: 'T002', trekName: 'Roopkund Trek', bookingDate: '2026-05-11', trekDates: '11 Jun - 18 Jun 2026', status: 'Booked' },
        { id: 'B003', userId: 'U003', userName: 'Rahul Verma', email: 'rahul@gmail.com', trekId: 'T004', trekName: 'Kedarkantha Trek', bookingDate: '2026-05-18', trekDates: '10 May - 14 May 2026', status: 'Cancelled' },
        { id: 'B004', userId: 'U001', userName: 'Amit Sharma', email: 'user@trekflow.com', trekId: 'T004', trekName: 'Kedarkantha Trek', bookingDate: '2026-05-09', trekDates: '10 May - 14 May 2026', status: 'Booked' }
      ]
    };
  },
  getters: {
    totalTreks: (state) => state.treks.length,
    totalUsers: (state) => state.users.length,
    totalStaff: (state) => state.staff.length,
    totalBookings: (state) => state.bookings.length,
    recentBookings: (state) => [...state.bookings].sort((a, b) => b.bookingDate.localeCompare(a.bookingDate)).slice(0, 6)
  },
  actions: {
    saveState() {
      localStorage.setItem('trekflow_state', JSON.stringify(this.$state));
    },
    login(email, password) {
      // Check Admin
      if (email === this.admin.email && password === this.admin.password) {
        this.currentUser = { ...this.admin };
        this.saveState();
        return { success: true, user: this.currentUser };
      }
      // Check Staff
      const staffMember = this.staff.find(s => s.email === email && s.password === password);
      if (staffMember) {
        if (staffMember.status === 'Blocked') {
          return { success: false, message: 'Your staff account has been blacklisted by the Admin.' };
        }
        this.currentUser = { ...staffMember };
        this.saveState();
        return { success: true, user: this.currentUser };
      }
      // Check Trekker
      const trekker = this.users.find(u => u.email === email && u.password === password);
      if (trekker) {
        if (trekker.status === 'Blocked') {
          return { success: false, message: 'Your account has been blacklisted. You cannot log in.' };
        }
        this.currentUser = { ...trekker };
        this.saveState();
        return { success: true, user: this.currentUser };
      }
      return { success: false, message: 'Invalid email or password.' };
    },
    logout() {
      this.currentUser = null;
      this.saveState();
    },
    register(name, email, password, contact) {
      if (this.users.some(u => u.email === email) || email === this.admin.email || this.staff.some(s => s.email === email)) {
        return { success: false, message: 'Email already registered.' };
      }
      const newTrekker = {
        id: 'U' + String(this.users.length + 1).padStart(3, '0'),
        name,
        email,
        password,
        contact,
        role: 'trekker',
        status: 'Active'
      };
      this.users.push(newTrekker);
      this.saveState();
      return { success: true, user: newTrekker };
    },
    createStaff(name, email, contact, password, experience, specialization) {
      if (this.staff.some(s => s.email === email) || email === this.admin.email || this.users.some(u => u.email === email)) {
        return { success: false, message: 'Email already exists.' };
      }
      const newStaff = {
        id: 'TS' + String(this.staff.length + 1).padStart(2, '0'),
        name,
        email,
        password,
        contact,
        role: 'staff',
        status: 'Active',
        experience: Number(experience),
        specialization
      };
      this.staff.push(newStaff);
      this.saveState();
      return { success: true };
    },
    blacklistUser(userId) {
      const user = this.users.find(u => u.id === userId);
      if (user) {
        user.status = 'Blocked';
        // Auto blacklist bookings if any
        this.saveState();
      }
    },
    whitelistUser(userId) {
      const user = this.users.find(u => u.id === userId);
      if (user) {
        user.status = 'Active';
        this.saveState();
      }
    },
    blacklistStaff(staffId) {
      const staffMember = this.staff.find(s => s.id === staffId);
      if (staffMember) {
        staffMember.status = 'Blocked';
        this.saveState();
      }
    },
    whitelistStaff(staffId) {
      const staffMember = this.staff.find(s => s.id === staffId);
      if (staffMember) {
        staffMember.status = 'Active';
        this.saveState();
      }
    },
    addTrek(name, location, difficulty, duration, startDate, endDate, slots, price, assignedStaffId, description) {
      const newTrek = {
        id: 'T' + String(this.treks.length + 1).padStart(3, '0'),
        name,
        location,
        difficulty,
        duration,
        startDate,
        endDate,
        slots: Number(slots),
        availableSlots: Number(slots),
        price: Number(price),
        status: 'Open',
        assignedStaffId,
        description,
        progress: 0,
        checkpoints: [
          { name: 'Base Camp', elevation: '4,000 ft' },
          { name: 'Camp 1', elevation: '6,500 ft' },
          { name: 'Camp 2', elevation: '9,000 ft' },
          { name: 'Summit', elevation: '12,000 ft' }
        ]
      };
      this.treks.push(newTrek);
      this.saveState();
    },
    editTrek(trekId, updatedTrek) {
      const index = this.treks.findIndex(t => t.id === trekId);
      if (index !== -1) {
        this.treks[index] = { ...this.treks[index], ...updatedTrek };
        this.saveState();
      }
    },
    deleteTrek(trekId) {
      this.treks = this.treks.filter(t => t.id !== trekId);
      // Cancel bookings related to this trek
      this.bookings.forEach(b => {
        if (b.trekId === trekId) {
          b.status = 'Cancelled';
        }
      });
      this.saveState();
    },
    bookTrek(trekId) {
      if (!this.currentUser) return { success: false, message: 'You must be logged in to book.' };
      
      const trek = this.treks.find(t => t.id === trekId);
      if (!trek) return { success: false, message: 'Trek not found.' };
      
      if (trek.availableSlots <= 0) return { success: false, message: 'No slots available.' };
      
      // Check if user already booked
      const existing = this.bookings.find(b => b.userId === this.currentUser.id && b.trekId === trekId && b.status === 'Booked');
      if (existing) return { success: false, message: 'You have already booked this trek.' };
      
      trek.availableSlots--;
      
      // Format trek dates
      const formatDateStr = (dateStr) => {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
      };
      
      const dateRangeStr = `${formatDateStr(trek.startDate)} - ${formatDateStr(trek.endDate)}`;
      
      const newBooking = {
        id: 'B' + String(this.bookings.length + 1).padStart(3, '0'),
        userId: this.currentUser.id,
        userName: this.currentUser.name,
        email: this.currentUser.email,
        trekId: trek.id,
        trekName: trek.name,
        bookingDate: new Date().toISOString().split('T')[0],
        trekDates: dateRangeStr,
        status: 'Booked'
      };
      
      this.bookings.push(newBooking);
      this.saveState();
      return { success: true };
    },
    cancelBooking(bookingId) {
      const booking = this.bookings.find(b => b.id === bookingId);
      if (booking) {
        booking.status = 'Cancelled';
        const trek = this.treks.find(t => t.id === booking.trekId);
        if (trek) {
          trek.availableSlots = Math.min(trek.slots, trek.availableSlots + 1);
        }
        this.saveState();
      }
    },
    updateTrekProgress(trekId, progress) {
      const trek = this.treks.find(t => t.id === trekId);
      if (trek) {
        trek.progress = Number(progress);
        this.saveState();
      }
    },
    completeTrek(trekId) {
      const trek = this.treks.find(t => t.id === trekId);
      if (trek) {
        trek.status = 'Completed';
        trek.progress = 100;
        // Update all related bookings to Completed
        this.bookings.forEach(b => {
          if (b.trekId === trekId && b.status === 'Booked') {
            b.status = 'Completed';
          }
        });
        this.saveState();
      }
    }
  }
});
