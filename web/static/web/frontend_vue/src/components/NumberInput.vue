<template>
  <div class="row text-center">
    <div class="row mb-2">
      <slider v-model="value" :min="this.min" :max="this.max" />
    </div>
    <div class="row">
      <div class="col-6">
      <div class="input-group mb-3">
        <span class="input-group-text px-1" id="from">От</span>
        <input type="number" v-model="value[0]" class="form-control px-1" aria-describedby="from">
      </div>
      </div>
      <div class="col-6">
      <div class="col-6 input-group  mb-3">
        <span class="input-group-text px-1" id="to">До</span>
        <input type="number" v-model="value[1]" class="form-control px-1" aria-describedby="to">
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import Slider from '@vueform/slider';

export default {
  name: "NumberInput",
  components: {
    Slider,
  },
  data() {
    return {
      value: [this.min, this.max]
    }
  },
  props: {
    min: {type: Number, default: 0},
    max: {type: Number, default: 100},
  },
  watch: {
    value: {
      handler(new_val) {
        if (new_val[0] < this.min) {
          this.value[0] = this.min;
        }
        if (new_val[1] > this.max) {
          this.value[1] = this.max;
        }
      },
      deep: true
    },
  },
}
</script>

<style src="@vueform/slider/themes/default.css"></style>
<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
}
</style>