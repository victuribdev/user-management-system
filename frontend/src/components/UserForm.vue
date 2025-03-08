<template>
  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title>
        {{ isEdit ? 'Edit User' : 'New User' }}
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" @submit.prevent="saveUser">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.username"
                  label="Username"
                  required
                  :rules="[v => !!v || 'Username is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12">
                <v-text-field
                  v-model="formData.password"
                  label="Password"
                  type="password"
                  required
                  :rules="[v => !!v || 'Password is required']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="12">
                <v-combobox
                  v-model="formData.roles"
                  label="Roles"
                  multiple
                  chips
                  :items="availableRoles"
                ></v-combobox>
              </v-col>
              
              <v-col cols="12">
                <v-select
                  v-model="formData.timezone"
                  label="Timezone"
                  :items="timezones"
                  required
                  :rules="[v => !!v || 'Timezone is required']"
                ></v-select>
              </v-col>
              
              <v-col cols="12">
                <v-switch
                  v-model="formData.active"
                  label="User Active"
                  color="primary"
                ></v-switch>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" text @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="saveUser" :disabled="!valid">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'UserForm',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      valid: false,
      formData: {
        username: '',
        password: '',
        roles: [],
        timezone: 'UTC',
        active: true
      },
      availableRoles: ['admin', 'manager', 'user', 'support', 'developer', 'tester'],
      timezones: [
        'Africa/Cairo',
        'America/Anchorage',
        'America/Buenos_Aires',
        'America/Chicago',
        'America/Los_Angeles',
        'America/New_York',
        'America/Phoenix',
        'Asia/Dubai',
        'Asia/Jakarta',
        'Asia/Tokyo',
        'Australia/Melbourne',
        'Australia/Sydney',
        'Europe/Berlin',
        'Europe/Dublin',
        'Europe/London',
        'Europe/Madrid',
        'Europe/Moscow',
        'Europe/Paris',
        'Pacific/Auckland',
        'UTC'
      ]
    }
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    },
    isEdit() {
      return !!this.user?._id
    }
  },
  watch: {
    modelValue(val) {
      if (val) {
        this.initForm()
      }
    }
  },
  methods: {
    initForm() {
      if (this.user) {
        this.formData = {
          _id: this.user._id,
          username: this.user.username,
          password: this.user.password,
          roles: [...this.user.roles],
          timezone: this.user.preferences.timezone,
          active: this.user.active
        }
      } else {
        this.formData = {
          username: '',
          password: '',
          roles: [],
          timezone: 'UTC',
          active: true
        }
      }
      
      this.$nextTick(() => {
        if (this.$refs.form) {
          this.$refs.form.resetValidation()
        }
      })
    },
    saveUser() {
      if (!this.valid) return
      
      this.$emit('save', this.formData)
    }
  }
}
</script> 