<script>
  import toast from "svelte-french-toast";
  import store from "../store/store";
  import axios from "axios";

  const BASEURL = import.meta.env.VITE_BASEURL;
  const CHAR_LIMITS = {
    title: { min: 10, max: 50 },
    shortDescription: { min: 50, max: 150 },
    longDescription: { min: 100, max: 2500 }
  };

  let loading = false;
  let data = {
    title: "",
    shortDescription: "",
    longDescription: "",
    githubLink: "",
    demoLink: "",
  };

  let count = {
    title: 0,
    shortDescription: 0,
    longDescription: 0,
  };

  $: {
    // Reactive updating of character counts
    Object.keys(count).forEach(key => {
      count[key] = data[key].length;
    });
  }

  function validateField(field, value) {
    const limits = CHAR_LIMITS[field];
    if (value.length < limits.min || value.length > limits.max) {
      toast.error(
        `${field.charAt(0).toUpperCase() + field.slice(1)} should be between ${limits.min} and ${limits.max} characters long`
      );
      return false;
    }
    return true;
  }

  function clearForm() {
    data = {
      title: "",
      shortDescription: "",
      longDescription: "",
      githubLink: "",
      demoLink: ""
    };
  }

  async function submit() {
    // Validate all required fields
    for (const field of Object.keys(CHAR_LIMITS)) {
      if (!validateField(field, data[field])) return;
    }

    if (loading) return;
    loading = true;

    try {
      const response = await axios.post(`${BASEURL}/create-project`, data);
      if (response.data.message === "Project created") {
        toast.success("Project created successfully");
        clearForm();
        $store.isAddModalOpen = false;
      } else {
        throw new Error("Invalid response");
      }
    } catch (error) {
      toast.error("Failed to create project. Please try again.");
    } finally {
      loading = false;
    }
  }
</script>

<input
  type="checkbox"
  bind:checked={$store.isAddModalOpen}
  class="modal-toggle"
/>

<div class="modal">
  <div class="modal-box max-w-3xl">
    <button
      on:click={() => ($store.isAddModalOpen = false)}
      class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
      aria-label="Close modal"
    >
      ✕
    </button>

    <h3 class="font-bold text-lg mb-4">Add a Hackathon Submission</h3>

    <div class="py-4 flex flex-col gap-4">
      <!-- Form Fields -->
      {#each ['title', 'shortDescription', 'longDescription'] as field}
        <div class="form-control">
          <div class="flex justify-between items-center mb-2">
            <label for={field} class="label-text-alt font-bold opacity-50 uppercase">
              Project {field.replace(/([A-Z])/g, ' $1').trim()}
            </label>
            <div class="text-sm">
              {count[field]}/{CHAR_LIMITS[field].max}
            </div>
          </div>
          
          {#if field === 'title'}
            <input
              id={field}
              bind:value={data[field]}
              type="text"
              class="input input-bordered w-full"
              placeholder={`Enter project ${field}`}
            />
          {:else}
            <textarea
              id={field}
              bind:value={data[field]}
              class="textarea textarea-bordered w-full"
              placeholder={field === 'shortDescription' 
                ? "Briefly explain what your project does"
                : "Explain your project in detail"}
            />
          {/if}
        </div>
      {/each}

      <!-- Links Section -->
      <div class="form-control">
        <label for="links-section" class="label-text-alt font-bold opacity-50 uppercase mb-2">Links</label>
        <div id="links-section" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="join w-full">
            <div class="join-item bg-slate-100 px-4 flex items-center">
              <!-- GitHub Icon -->
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 h-6">
                <path fill="currentColor" d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </div>
            <input
              type="url"
              bind:value={data.githubLink}
              class="join-item input input-bordered flex-1"
              placeholder="GitHub Repository Link"
            />
          </div>

          <div class="join w-full">
            <div class="join-item bg-slate-100 px-4 flex items-center">
              <!-- Demo Link Icon -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                class="w-6 h-6"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5"
                />
              </svg>
            </div>
            <input
              type="url"
              bind:value={data.demoLink}
              class="join-item input input-bordered flex-1"
              placeholder="Live Demo Link"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-4 mt-6">
      <button
        class="btn btn-ghost"
        on:click={clearForm}
        type="button"
      >
        Clear
      </button>
      <button
        on:click={submit}
        disabled={loading}
        class="btn btn-primary ml-auto"
        type="submit"
      >
        {#if loading}
          <div class="loading loading-spinner" />
        {:else}
          Submit
        {/if}
      </button>
    </div>
  </div>
</div>

