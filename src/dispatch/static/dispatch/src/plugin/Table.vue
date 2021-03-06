<template>
  <v-layout wrap>
    <new-edit-sheet />
    <div class="headline">Plugins</div>
    <v-spacer />
    <v-flex xs12>
      <v-layout column>
        <v-flex>
          <v-card>
            <v-card-title>
              <v-text-field
                v-model="q"
                append-icon="search"
                label="Search"
                single-line
                hide-details
                clearable
                :loading="loading"
              />
            </v-card-title>
            <v-data-table
              :headers="headers"
              :items="items"
              :server-items-length="total"
              :page.sync="page"
              :items-per-page.sync="itemsPerPage"
              :sort-by.sync="sortBy"
              :sort-desc.sync="descending"
              @click:row="editShow"
            >
              <template v-slot:item.author="{ item }">
                <a :href="item.author_url" target="_blank" style="text-decoration: none;">
                  {{ item.author }}
                  <v-icon small>open_in_new</v-icon>
                </a>
              </template>
              <template v-slot:item.enabled="{ item }">
                {{ item.enabled ? "Enabled" : "Disabled" }}
              </template>
              <template v-slot:item.multiple="{ item }">
                {{ item.multiple ? "Yes" : "No" }}
              </template>
              <template v-slot:item.required="{ item }">
                {{ item.required ? "Yes" : "No" }}
              </template>
            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapFields } from "vuex-map-fields"
import { mapActions } from "vuex"
import NewEditSheet from "@/plugin/editSheet.vue"
export default {
  name: "PluginTable",

  components: {
    NewEditSheet
  },
  data() {
    return {
      headers: [
        { text: "Title", value: "title", sortable: true },
        { text: "Slug", value: "slug", sortable: true },
        { text: "Author", value: "author", sortable: true },
        { text: "Version", value: "version", sortable: true },
        { text: "Status", value: "enabled", sortable: true },
        { text: "Required", value: "required", sortable: true },
        { text: "Multiple Allowed", value: "multiple", sortable: true },
        { text: "Type", value: "type", sortable: true }
      ]
    }
  },

  computed: {
    ...mapFields("plugin", [
      "table.options.q",
      "table.options.page",
      "table.options.itemsPerPage",
      "table.options.sortBy",
      "table.options.descending",
      "table.options.loading",
      "table.rows.items",
      "table.rows.total"
    ])
  },

  mounted() {
    this.getAll({})

    this.$watch(
      vm => [vm.q, vm.page, vm.itemsPerPage, vm.sortBy, vm.descending],
      () => {
        this.getAll()
      }
    )
  },

  methods: {
    ...mapActions("plugin", ["getAll", "editShow"])
  }
}
</script>
