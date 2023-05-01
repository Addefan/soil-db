import {createStore} from "vuex";
import axios from "axios";
import qs from "qs";

const store = createStore({
    state() {
        return {
            attributes: [],
            plants: [],
            parameters: {
                page: 1,
            },
            isLoadingAttributes: false,
        }
    },
    getters: {
        getQueryParams: (state) => {
            return `?${qs.stringify(state.parameters, { indices: false })}`
        }
    },
    actions: {
        async loadPlants({ commit }, queryParams = "") {
            // TODO сделайте функцию load, которая будет грузить страницу, указанную в сторе
            //  затем сделайте функцию loadMore, которая будет делать page++ и дергать load()
            try {
                commit("INCREASE_PAGE");
                const response = await axios.get(`/api/plants${queryParams}`);
                commit("SET_PLANTS", { new_plants: response.data });
            } catch (e) {
                // TODO убрать костыль
                if (e.response.data === "Неправильная страница") {
                    console.log("No more plants to load");
                }
                else {
                    commit("DECREASE_PAGE");
                }
            }
        },
        async loadAttributes({commit}) {
            commit("SWITCH_ATTRIBUTES_LOADING");
            const response = await axios.get("/api/attributes/");
            commit("SET_ATTRIBUTES", response.data);
            commit("SWITCH_ATTRIBUTES_LOADING");
        },
    },
    mutations: {
        SET_ATTRIBUTES(state, new_attributes) {
            state.attributes = new_attributes;
        },
        SET_PLANTS(state, {new_plants, reset = false}) {
            if (reset) {
                state.plants = new_plants;
            }
            else {
                state.plants = [...state.plants, ...new_plants];
            }
        },
        SET_PARAMETER(state, {param, values}) {
            state.parameters[param] = values;
        },
        SET_PARAMETERS(state, {parameters}) {
            state.parameters = parameters;
        },
        INCREASE_PAGE(state) {
            state.parameters.page++;
        },
        DECREASE_PAGE(state) {
            state.parameters.page--;
        },
        SWITCH_ATTRIBUTES_LOADING(state) {
            state.isLoadingAttributes = !state.isLoadingAttributes;
        }
    }
})

export default store
