<template>
  <section>
    <div>
      <select v-model="selectedValue" @change="onChange(selectedValue)">
        <option disabled value>Please select one</option>
        <option
            v-for="(locale, index) in $i18n.locales"
            :key="index"
            :value="locale.code"
        >{{ locale.name }}
        </option>
      </select>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      selectedValue: ""
    };
  },
  created() {
    this.selectedValue = this.$i18n.locale;
  },
  methods: {
    onChange(event) {
      this.$router.replace(this.switchLocalePath(event));
    }
  }
};
</script>

<style scoped>
.subtitle {
  font-weight: 300;
  font-size: 3em;
  color: #2E495E;
  word-spacing: 5px;
  padding-bottom: 15px;
  margin-top: 200px;
}
</style>
