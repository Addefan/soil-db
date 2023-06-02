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
            isMorePlants: true,
            isLoading: false,
            previousParameters: null,
        }
    },
    getters: {
        getQueryParams: (state) => {
            return `?${qs.stringify(state.parameters, { indices: false })}`
        }
    },
    actions: {
        async loadPlants({ commit, getters }) {
            commit("SET_IS_LOADING", true);
            try {
                commit("SWITCH_IS_MORE_PLANTS");
                const response = await axios.get(`/api/plants${getters.getQueryParams}`);
                commit("SET_PREVIOUS_PARAMETERS", getters.getQueryParams);
                commit("SET_PLANTS", { new_plants: response.data.results });
                if (response.data.next) {
                    commit("SWITCH_IS_MORE_PLANTS");
                    commit("INCREASE_PAGE");
                }
            } catch (e) {
                commit("SET_PREVIOUS_PARAMETERS", null);
                console.error(e);
            }
            commit("SET_IS_LOADING", false);
        },
        async loadMore({ state, dispatch }) {
            if (state.isMorePlants) {
                await dispatch("loadPlants");
            }
        },
        async loadAttributes({commit}) {
            commit("SET_IS_LOADING", true);
            const response = await axios.get("/api/attributes/");
            commit("SET_ATTRIBUTES", response.data);
            commit("SET_IS_LOADING", false);
        },
    },
    mutations: {
        SET_ATTRIBUTES(state, new_attributes) {
            state.attributes = new_attributes;
        },
        SWITCH_IS_MORE_PLANTS(state) {
          state.isMorePlants = !state.isMorePlants;
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
        SET_IS_LOADING(state, value) {
            state.isLoading = value;
        },
        SET_PREVIOUS_PARAMETERS(state, value) {
            state.previousParameters = value;
        }
    }
})

export default store
