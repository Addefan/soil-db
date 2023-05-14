<template>
  <VueDatePicker v-model="date" range locale="ru" cancelText="Закрыть" selectText="Выбрать"
                 :enable-time-picker="false" :preview-format="previewFormat"
                 partial-range :partial-range="false" placeholder="Pick some"
                 :format="format">
  </VueDatePicker>
</template>

<script>
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { mapMutations, mapState } from "vuex";

export default {
  components: { VueDatePicker },
  name: "CustomDateFilter",
  props: {
    attrName: {
      type: String,
      required: true,
    }
  },
  data() {
    const convertDateComponent = (component) => {
      return +component < 10 ? `0${component}` : component;
    }
    const beautifyDate = (date) => {
      const startDay = convertDateComponent(date.getDate());
      const startMonth = convertDateComponent(date.getMonth() + 1);
      const startYear = date.getFullYear();
      return `${startDay}.${startMonth}.${startYear}`
    }
    return {
      format(date) {
        return this.previewFormat(date).join(" — ");
      },
      previewFormat(date) {
        return date.map(elem => beautifyDate(elem));
      }
    }
  },
  methods: {
    ...mapMutations({setParameter: "SET_PARAMETER"})
  },
  computed: {
    date: {
      set(value) {
        this.setParameter({ param: this.attrName, values: value ?? [] });
      },
      get() {
        return this.parameters[this.attrName];
      }
    },
    ...mapState(["parameters"])
  }
};
</script>

<style>
  @import "@vuepic/vue-datepicker/dist/main.css";
  input.dp__pointer.dp__input_readonly.dp__input.dp__input_icon_pad.dp__input_reg {
    font-size: 14px;
  }

</style>
