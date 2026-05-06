{ lib }:
{
  # Merge a list of dev environment attribute sets into one.
  # Each env may have: packages (list), shellHook (string).
  mergeDevEnvs = envList: {
    packages  = lib.concatMap (e: e.packages  or []) envList;
    shellHook = lib.concatStrings (map (e: e.shellHook or "") envList);
  };
}
