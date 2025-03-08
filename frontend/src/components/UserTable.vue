<template>
  <v-data-table
    :headers="headers"
    :items="users"
    :sort-by="[{ key: 'username', order: 'asc' }]"
    class="elevation-1"
  >
    <template v-slot:item.username="{ item }">
      <router-link :to="`/user/${item._id}`">
        {{ item.username }}
      </router-link>
    </template>

    <template v-slot:item.roles="{ item }">
      <v-chip
        v-for="role in item.roles"
        :key="role"
        class="mr-1"
        color="primary"
        size="small"
      >
        {{ role }}
      </v-chip>
    </template>

    <template v-slot:item.timezone="{ item }">
      {{ getTimezone(item) }}
    </template>

    <template v-slot:item.active="{ item }">
      <v-chip
        :color="item.active ? 'success' : 'error'"
        size="small"
      >
        {{ item.active ? 'Yes' : 'No' }}
      </v-chip>
    </template>

    <template v-slot:item.updated_ts="{ item }">
      {{ formatDate(item.updated_ts) }}
    </template>

    <template v-slot:item.created_ts="{ item }">
      {{ formatDate(item.created_ts) }}
    </template>

    <template v-slot:item.preferences.timezone="{ item }">
      {{ item.preferences?.timezone || item.user_timezone || 'UTC' }}
    </template>

    <template v-slot:item.actions="{ item }">
      <v-icon
        size="small"
        class="mr-2"
        @click="$emit('edit-user', item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        size="small"
        color="error"
        @click="$emit('delete-user', item)"
      >
        mdi-delete
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: 'UserTable',
  props: {
    users: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      headers: [
        { title: 'Username', key: 'username', sortable: true },
        { title: 'Roles', key: 'roles', sortable: false },
        { title: 'Timezone', key: 'preferences.timezone', sortable: true },
        { title: 'Active?', key: 'active', sortable: true },
        { title: 'Last Updated', key: 'updated_ts', sortable: true },
        { title: 'Created At', key: 'created_ts', sortable: true },
        { title: 'Actions', key: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      return new Date(timestamp * 1000).toLocaleString()
    },
    getTimezone(item) {
      if (item.preferences && item.preferences.timezone) {
        return item.preferences.timezone;
      }
      if (item.timezone) {
        return item.timezone;
      }
      return 'UTC';
    }
  }
}
</script> 