import ConfigureHackathon from "./src/pages/ConfigureHackathon.svelte";
import Home from "./src/pages/Home.svelte";
import ProjectInfo from "./src/pages/ProjectInfo.svelte";
import Search from "./src/pages/Search.svelte";

const routes = {
  "/": Home,
  "/project/:id": ProjectInfo,
  "/config": ConfigureHackathon,
  "/search/:id": Search,
};
export default routes;
