<template>
  <div>
    <v-card class="mb-5">
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Manage Users</span>
        <v-btn color="primary" @click="openUserForm()">
          <v-icon left>mdi-plus</v-icon>
          New User
        </v-btn>
      </v-card-title>
      <v-card-text>
        <user-table 
          :users="users" 
          @edit-user="openUserForm" 
          @delete-user="confirmDelete"
          @refresh="fetchUsers"
        />
      </v-card-text>
    </v-card>

    <user-form
      v-model="showUserForm"
      :user="currentUser"
      @save="saveUser"
    />

    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete user "{{ userToDelete?.username }}"?
          This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="confirmDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteUser">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import UserTable from '../components/UserTable.vue'
import UserForm from '../components/UserForm.vue'
import axios from 'axios'

export default {
  name: 'HomeView',
  components: {
    UserTable,
    UserForm
  },
  data() {
    return {
      users: [],
      showUserForm: false,
      currentUser: null,
      confirmDeleteDialog: false,
      userToDelete: null
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        console.log("Attempting to fetch users...");
        const url = 'http://localhost:5000/api/users';
        console.log("Request URL:", url);
        const response = await axios.get(url);
        console.log("Response received:", response.data);
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    openUserForm(user = null) {
      this.currentUser = user
      this.showUserForm = true
    },
    async saveUser(userData) {
      try {
        if (userData._id) {
          await axios.put(`http://localhost:5000/api/users/${userData._id}`, userData)
        } else {
          await axios.post('http://localhost:5000/api/users', userData)
        }
        this.fetchUsers()
        this.showUserForm = false
      } catch (error) {
        console.error('Error saving user:', error)
      }
    },
    confirmDelete(user) {
      this.userToDelete = user
      this.confirmDeleteDialog = true
    },
    async deleteUser() {
      try {
        await axios.delete(`http://localhost:5000/api/users/${this.userToDelete._id}`)
        this.fetchUsers()
        this.confirmDeleteDialog = false
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    }
  }
}
</script> 