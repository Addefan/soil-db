<template>
  <VueDatePicker v-model="date" range locale="ru" cancelText="Закрыть" selectText="Выбрать"
                 :enable-time-picker="false"></VueDatePicker>
</template>

<script>
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { mapGetters, mapMutations } from "vuex";

export default {
  components: { VueDatePicker },
  name: "CustomDateFilter",
  props: {
    attrName: {
      type: String,
      required: true
    }
  },
  methods: {
    ...mapGetters(["getParameters"]),
    ...mapMutations(["SET_PARAMETER"])
  },
  computed: {
    date: {
      set(value) {
        this.$store.commit("SET_PARAMETER", { param: this.attrName, values: value ?? [] });
      },
      get() {
        return this.getParameters()[this.attrName];
      }
    }
  }
};
</script>

<style scoped>

</style>