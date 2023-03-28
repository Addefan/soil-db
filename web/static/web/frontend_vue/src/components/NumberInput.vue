<template>
  <slider v-model="value" @end="showValue" :min="this.min" :max="this.max" />
</template>

<script>
import Slider from '@vueform/slider';

export default {
  name: "NumberInput",
  components: {
    Slider
  },
  data() {
    return {
      value: [this.min, this.max],
    }
  },
  methods: {
    showValue() {
      console.log(this.value)
    }
  },
  props: {
    min: {type: Number, default: 0},
    max: {type: Number, default: 100}
  }
}
</script>

<style src="@vueform/slider/themes/default.css"></style>
<style scoped>

</style>