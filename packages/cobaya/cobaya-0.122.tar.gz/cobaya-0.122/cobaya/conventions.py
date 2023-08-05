"""
.. module:: conventions

:Synopsis: Some naming conventions to make the life of the maintainer easier.
:Author: Jesus Torrado

"""
# Package name (for importlib)
# (apparently __package__ is only defined if you import something locally.
package = __name__.rpartition('.')[0]

# Names for block and fields in the input
_likelihood = "likelihood"
_prior      = "prior"
_theory     = "theory"
_sampler    = "sampler"
_params     = "params"
_p_dist     = "dist"
_p_ref      = "ref"
_p_label    = "latex"
_p_drop     = "drop"
_p_derived  = "derived"
_p_proposal = "proposal"
_debug      = "debug"
_debug_file = "debug_file"
_output_prefix = "output_prefix"
_path_install = "path_to_modules"
_external = "external"

# Separator for different names.
# Its manual inclusion in a string anywhere else (e.g. a parameter name) is forbidden.
separator = "__"

# Names for the samples' fields internally and in the output
_weight        = "weight"        # sample weight
_minuslogpost  = "minuslogpost"  # log-posterior, or in general the total log-probability
_minuslogprior = "minuslogprior" # log-prior
_chi2          = "chi2"          # chi^2 = -2 * loglik
_derived_pre   = "derived"+separator  # prefix for derived parameters

# Output files
_input_suffix = "input"
_full_suffix  = "full"

# Internal package structure
_defaults_file = "defaults.yaml"
subfolders = {_likelihood: "likelihoods",
              _sampler: "samplers",
              _theory: "theories"}
