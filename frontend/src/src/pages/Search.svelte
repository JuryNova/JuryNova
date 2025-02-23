<script>
  import { onMount } from "svelte";
  import ModalWrapper from "../components/ModalWrapper.svelte";
  import Nav from "../components/Nav.svelte";
  import ProjectCard from "../components/ProjectCard.svelte";
  import axios from "axios";
  import { getRandomLoadingMessage } from "../store/loading";

  export let params;
  
  const BASEURL = import.meta.env.VITE_BASEURL;
  
  let data = {
    projects: [],
  };
  let loading = false;
  let error = null;

  async function searchProjects(query) {
    try {
      loading = true;
      error = null;
      const response = await axios.post(`${BASEURL}/search`, { query });
      data.projects = response.data.projects;
    } catch (err) {
      error = err.response?.data?.message || 'An error occurred while searching';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    if (params.id) {
      searchProjects(params.id);
    }
  });
</script>

<ModalWrapper>
  <div class="container mx-auto p-3 md:p-5 lg:p-10">
    <Nav />
    
    <div class="flex flex-col gap-6 mt-6">
      <h1 class="text-2xl font-medium">
        Searching for: <span class="font-semibold text-primary">{params.id}</span>
      </h1>

      {#if error}
        <div class="alert alert-error shadow-lg">
          <span>{error}</span>
        </div>
      {/if}

      <section class="grid gap-5 grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
        {#if loading}
          <div class="col-span-full min-h-[60vh] flex flex-col items-center justify-center gap-4">
            <div class="loading loading-spinner loading-lg" />
            <p class="max-w-xs text-base text-center text-gray-600">
              {getRandomLoadingMessage()}
            </p>
          </div>
        {:else if data.projects.length === 0}
          <div class="col-span-full min-h-[60vh] flex flex-col items-center justify-center">
            <p class="text-lg text-gray-600">No projects found matching your search.</p>
          </div>
        {:else}
          {#each data.projects as project, index (project._id)}
            <ProjectCard
              description={project.shortDescription}
              title={project.title}
              id={project._id}
              isReviewed={project.isReviewed}
              index={index + 1}
            />
          {/each}
        {/if}
      </section>
    </div>
  </div>
</ModalWrapper>

<style>
  .container {
    max-width: 1440px;
  }
</style>