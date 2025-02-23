<script>
  import { onMount } from "svelte";
  import ModalWrapper from "../components/ModalWrapper.svelte";
  import Nav from "../components/Nav.svelte";
  import ProjectCard from "../components/ProjectCard.svelte";
  import axios from "axios";
  import { getRandomLoadingMessage } from "../store/loading";

  const BASEURL = import.meta.env.VITE_BASEURL;
  
  // Reactive declarations
  $: projects = [];
  let loading = false;
  let error = null;

  async function fetchProjects() {
    loading = true;
    error = null;
    
    try {
      const response = await axios.get(`${BASEURL}/get-all`);
      projects = response.data.projects;
    } catch (err) {
      error = err.message || 'Failed to fetch projects';
    } finally {
      loading = false;
    }
  }

  onMount(fetchProjects);
</script>

<ModalWrapper>
  <div class="container mx-auto p-3 md:p-5 lg:p-10">
    <Nav />
    <main>
      <section 
        class="grid gap-5 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 mt-10"
        aria-label="Projects gallery"
      >
        {#if loading}
          <div
            class="flex col-span-full flex-col gap-3 h-[80vh] justify-center items-center"
            role="status"
          >
            <span class="loading loading-spinner loading-md" aria-hidden="true" />
            <p class="max-w-xs text-sm text-center text-gray-600">
              {getRandomLoadingMessage()}
            </p>
          </div>
        {:else if error}
          <div class="col-span-full text-center text-red-600 py-10">
            <p>Error: {error}</p>
            <button
              class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              on:click={fetchProjects}
            >
              Retry
            </button>
          </div>
        {:else if projects.length === 0}
          <div class="col-span-full text-center text-gray-600 py-10">
            <p>No projects found.</p>
          </div>
        {:else}
          {#each projects as project (project._id)}
            <ProjectCard
              description={project.shortDescription}
              title={project.title}
              id={project._id}
              isReviewed={project.isReviewed}
            />
          {/each}
        {/if}
      </section>
    </main>
  </div>
</ModalWrapper>

<style>
  .container {
    max-width: 1440px;
  }
  
  .loading {
    color: theme('colors.blue.500');
  }
</style>