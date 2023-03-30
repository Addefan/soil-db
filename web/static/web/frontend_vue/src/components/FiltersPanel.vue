<template>
  <div class="rounded-4 h-100 mh-50 table-color">
    <form @submit.prevent="submitEvent">
      <div v-for="param in this.getParameters()" :key="param" class="pt-1 px-2">
        {{ param.russian_name }}
        <div v-if="param.type === 'text'">
          <SearchSelect :variants="param.values" @change="logConsole"></SearchSelect>
        </div>
        <!--TODO: component depending on parameter type-->
      </div>
      <div class="text-center buttons position-sticky top-100 mb-1">
        <button class="btn btn-success btn-sm me-1">
          Применить
        </button>
        <button type="button" class="btn btn-outline-success ms-1 btn-sm mx-auto export_to_xlsx__button"
                data-bs-toggle="modal" data-bs-target="#ModalXlsx">Экспорт
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import SearchSelect from "@/components/SearchSelect.vue";

export default {
  name: "FiltersPanel",
  data() {
    return {
      value: {},
    }
  },
  components: {SearchSelect},
  methods: {
    ...mapActions(["loadParameters"]),
    ...mapGetters(["getParameters"]),

  },
  mounted() {
    this.loadParameters();
  }
}
</script>

<style scoped>
.buttons {
  position: relative
}

.filters {

}
</style>