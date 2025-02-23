<script>
  import toast from "svelte-french-toast";
  import store from "../store/store";
  import Papa from "papaparse";
  import axios from "axios";

  const BASEURL = import.meta.env.VITE_BASEURL;
  const VALIDATION_RULES = {
    title: { min: 10, max: 50 },
    shortDescription: { min: 50, max: 150 },
    longDescription: { min: 100, max: 2500 }
  };

  let file = null;
  let loading = false;

  const isValidProject = (project) => {
    return (
      project.title.length >= VALIDATION_RULES.title.min &&
      project.title.length <= VALIDATION_RULES.title.max &&
      project.shortDescription.length >= VALIDATION_RULES.shortDescription.min &&
      project.shortDescription.length <= VALIDATION_RULES.shortDescription.max &&
      project.longDescription.length >= VALIDATION_RULES.longDescription.min &&
      project.longDescription.length <= VALIDATION_RULES.longDescription.max
    );
  };

  async function sendToServer(data) {
    try {
      const response = await axios.post(`${BASEURL}/create-project`, data);
      if (response.data.message === "Project created") {
        toast.success("Project created successfully");
      }
    } catch (error) {
      toast.error(error.response?.data?.message || "Failed to create project");
    }
  }

  async function handleFileSubmit() {
    if (!file?.[0]) {
      toast.error("Please select a file");
      return;
    }

    loading = true;
    
    Papa.parse(file[0], {
      header: true,
      complete: async function (results) {
        try {
          const validProjects = results.data
            .filter((_, index) => !results.errors.some(error => error.row === index))
            .map((item) => ({
              title: item["Title"]?.trim(),
              shortDescription: item["Short Description"]?.trim(),
              longDescription: item["Long Description"]?.trim(),
              githubLink: item["Github Link"]?.trim(),
              demoLink: item["Demo Link"]?.trim(),
            }))
            .filter(project => {
              if (!isValidProject(project)) {
                toast.error(`Invalid project: ${project.title}`);
                return false;
              }
              return true;
            });

          for (const project of validProjects) {
            await sendToServer(project);
          }
        } catch (error) {
          toast.error("Error processing CSV file");
        } finally {
          loading = false;
        }
      },
      error: (error) => {
        toast.error("Error parsing CSV file");
        loading = false;
      }
    });
  }
</script>

<input
  type="checkbox"
  bind:checked={$store.isAddCSVModalOpen}
  class="modal-toggle"
/>

<div class="modal">
  <div class="modal-box max-w-3xl">
    <button
      on:click={() => ($store.isAddCSVModalOpen = false)}
      class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      aria-label="Close modal"
    >
      ✕
    </button>
    
    <h3 class="font-bold text-lg mb-4">Add Multiple Hackathon Submissions</h3>
    
    <div class="py-4 flex flex-col gap-3">
      <input
        type="file"
        accept=".csv"
        bind:files={file}
        class="file-input file-input-bordered w-full"
      />
      <p class="label-text-alt">Upload a CSV file</p>
    </div>

    <div class="flex items-center gap-4">
      <button 
        on:click={() => (file = null)} 
        class="btn btn-ghost"
        disabled={loading}
      >
        Clear
      </button>
      
      <button
        on:click={handleFileSubmit}
        disabled={loading || !file}
        class="btn btn-primary btn-circle ml-auto"
        aria-label={loading ? 'Loading' : 'Submit'}
      >
        {#if loading}
          <div class="loading loading-spinner" />
        {:else}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
            />
          </svg>
        {/if}
      </button>
    </div>

    <div class="mt-4 p-4 bg-base-200 rounded-lg">
      <p class="mb-2">
        This feature has been disabled to preserve resources. Please view the
        video submission to see how to add multiple projects.
      </p>
      <a
        href="https://youtu.be/8UYPhdfQ1-w"
        target="_blank"
        rel="noopener noreferrer"
        class="btn btn-sm btn-secondary"
      >
        Watch Tutorial
      </a>
    </div>
  </div>
</div>