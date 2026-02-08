⟦CRUX:configManager.ts
Ρ{archetype cfg mgr;TS;Node;loads plugins+rules+exemptions}

Κ{axios,log,pluginReg,opts,fs,path;Types=@x-fidelity/types;
  CentralCfgMgr=../config/centralConfigManager}

Φ{REPO_GLOBAL_CHECK;MAX_RETRIES=3;RETRY_DELAY=1000}

E{ExecutionConfig{archetype;rules;cliOptions;exemptions};
  configs:Map<arch,ExecutionConfig>}

Λ.repoDir{→test?'/repo':opts.dir}
Λ.getLoadedConfigs{→keys(configs)}
Λ.clearLoadedConfigs{∀k→del configs[k]}

Λ.getConfig{params→ExecutionConfig;
  arch=params.archetype|opts.archetype|'node-fullstack';
  ¬configs[arch]→initialize»cache;→configs[arch]}

Λ.dynamicImport{path→import(path)}
Λ.getPluginRegistryName{name→xfiPlugin*?kebab:as-is}
Λ.filterUnloadedPlugins{names→∀n»check reg»skip loaded}

Λ.loadPlugins{exts?→void;¬exts→return;
  builtins←@x-fidelity/plugins.getBuiltinPluginNames()|fallback;
  ∀mod{builtin?→load+register;test→skip;
    else→try[yarn global→local→pkg→legacy]»register};
  await pluginReg.waitForAllPlugins()}

Γ.initialize{params→ExecutionConfig;
  arch,logPrefix←params;cfgServer,localPath,ghLoc←opts;
  cfg={archetype:{},rules:[],cliOpts,exemptions:[]};
  
  centralCfgMgr.init();wsRoot=findWsRoot();
  allowedPaths←ConfigSetMgr+CentralCfgMgr.updateSecurityPaths([
    cwd,wsRoot,packages,dist,/tmp,democonfig,fixtures,temp]);
  security.updateAllowedPaths();
  
  resolution←centralCfgMgr.resolveConfigPath({arch,cfgServer,localPath,ghLoc,wsRoot});
  resolution.src='configServer'→fetchRemote;else→loadLocal;
  ¬cfg.archetype→throw;
  
  basePlugins»loadPlugins;extraPlugins»filter»loadPlugins;
  archPlugins»filter»loadPlugins;
  
  rules=obj[]?direct:loadRules();∀rule→validate»filter;
  exemptions←loadExemptions();→cfg}

Λ.fetchRemoteConfig{cfgServer,arch,prefix?→ArchetypeConfig;
  url=cfgServer+'/archetypes/'+arch;
  retry(3,1s){axios.get»validate→cfg|throw}»throw max}

Λ.loadLocalConfig{params→ArchetypeConfig;arch,path←params;
  validate arch name;¬path→throw;normalize+resolve;
  ..|\0→throw traversal;findWsRoot();
  allowedPaths←ConfigSetMgr+CentralCfgMgr.updateSecurityPaths();
  ¬path∈allowed→throw;sanitize→cfgPath=resolved/arch.json;
  ¬starts(resolved)→throw;content←read»parse»validate→cfg}

Λ.loadBuiltinConfig{arch→ArchetypeConfig;validate name;
  paths=[__dirname/demoConfig,cwd/packages/*/dist/demoConfig,fallbacks];
  ∀p→try access»first found;¬found→throw;
  content←read»parse»validate→cfg}

P.err{init→log+rethrow;fetch→retry»throw;load→log+rethrow;
  traversal|invalid name→throw;plugin fail→log+throw}
P.security{name=/^[a-zA-Z0-9-_]+$/;path∈allowed;¬..|\0;startsWith}

M{configs:static Map;pluginRegistry→shared}

Ω.decomp{emulate=tsc --strict;src=ts;
  focus=[async/await,static methods,path security,retry,dynamic import]}
⟧
