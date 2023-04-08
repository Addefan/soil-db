<template>
  <div>
    <Multiselect v-model="value" :options="variants" :multiple="true" :close-on-select="false"
                 :clear-on-select="false" :preserve-search="true" placeholder="Pick some"
                 :select-label="''" :deselect-label="''">
    </Multiselect>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "SearchSelect",
  components: {
    Multiselect
  },
  computed: {
    value: {
      set(value) {
        this.$store.commit("SET_PARAMETER", { param: this.attrName, values: value });
      },
      get() {
        return this.getParameters()[this.attrName] ?? [];
      }
    }
  },
  props: {
    variants: Array,
    attrName: { type: String, required: true }
  },
  methods: {
    ...mapGetters(["getParameters"]),
    ...mapMutations(["SET_PARAMETER"])
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>