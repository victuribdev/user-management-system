<template>
  <div v-if="user">
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>User Details: {{ user.username }}</span>
        <div>
          <v-btn color="primary" class="mr-2" @click="editUser">
            <v-icon left>mdi-pencil</v-icon>
            Edit
          </v-btn>
          <v-btn color="error" @click="confirmDelete">
            <v-icon left>mdi-delete</v-icon>
            Delete
          </v-btn>
        </div>
      </v-card-title>
      
      <v-card-text>
        <v-list>
          <v-list-item>
            <v-list-item-title>Username:</v-list-item-title>
            <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item>
            <v-list-item-title>Roles:</v-list-item-title>
            <v-list-item-subtitle>
              <v-chip v-for="role in user.roles" :key="role" class="mr-1" color="primary" small>
                {{ role }}
              </v-chip>
            </v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item>
            <v-list-item-title>Timezone:</v-list-item-title>
            <v-list-item-subtitle>{{ user.preferences.timezone }}</v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item>
            <v-list-item-title>Active:</v-list-item-title>
            <v-list-item-subtitle>
              <v-chip :color="user.active ? 'success' : 'error'" small>
                {{ user.active ? 'Yes' : 'No' }}
              </v-chip>
            </v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item>
            <v-list-item-title>Created At:</v-list-item-title>
            <v-list-item-subtitle>{{ formatDate(user.created_ts) }}</v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item v-if="user.updated_ts">
            <v-list-item-title>Last Updated:</v-list-item-title>
            <v-list-item-subtitle>{{ formatDate(user.updated_ts) }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <user-form
      v-model="showUserForm"
      :user="user"
      @save="saveUser"
    />

    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete user "{{ user.username }}"?
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
  <div v-else>
    <v-progress-circular indeterminate color="primary"></v-progress-circular>
  </div>
</template>

<script>
import UserForm from '../components/UserForm.vue'
import axios from 'axios'

export default {
  name: 'UserView',
  components: {
    UserForm
  },
  data() {
    return {
      user: null,
      showUserForm: false,
      confirmDeleteDialog: false
    }
  },
  created() {
    this.fetchUser()
  },
  methods: {
    async fetchUser() {
      try {
        const response = await axios.get(`http://localhost:5000/api/users/${this.$route.params.id}`)
        this.user = response.data
      } catch (error) {
        console.error('Error fetching user:', error)
      }
    },
    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      return new Date(timestamp * 1000).toLocaleString()
    },
    editUser() {
      this.showUserForm = true
    },
    async saveUser(userData) {
      try {
        await axios.put(`http://localhost:5000/api/users/${this.user._id}`, userData)
        this.fetchUser()
        this.showUserForm = false
      } catch (error) {
        console.error('Error saving user:', error)
      }
    },
    confirmDelete() {
      this.confirmDeleteDialog = true
    },
    async deleteUser() {
      try {
        await axios.delete(`http://localhost:5000/api/users/${this.user._id}`)
        this.confirmDeleteDialog = false
        this.$router.push('/')
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    }
  }
}
</script> 