<template>
  <VueDatePicker v-model="date" range locale="ru" cancelText="Закрыть" selectText="Выбрать"
                 :enable-time-picker="false" :preview-format="previewFormat"
                 partial-range :partial-range="false" placeholder="Pick some"
                 :format="format" @update:model-value="$emit('change', date ?? [])">
  </VueDatePicker>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
export default {
  data() {
    const convertDateComponent = (component) => {
      return +component < 10 ? `0${component}` : component;
    }
    const beautifyDate = (date) => {
      const startDay = convertDateComponent(date.getDate());
      const startMonth = convertDateComponent(date.getMonth() + 1);
      const startYear = convertDateComponent(date.getFullYear());
      return `${startDay}.${startMonth}.${startYear}`
    }
    return {
      date: [],
      format(date) {
        date = date.map(elem => beautifyDate(elem));
        return date.join(" — ");
      },
      previewFormat(date) {
        return date.map(elem => beautifyDate(elem));
      }
    }
  },
  components: {VueDatePicker},
  name: "CustomDateFilter"
}
</script>

<style scoped>

</style>