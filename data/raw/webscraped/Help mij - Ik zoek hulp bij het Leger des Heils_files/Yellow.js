/**
 * Yellow
 * enrich html with javascript in a clean, non-complicated way
 * Yellow uses jquery, so include that before Yellow. Config is done through data- attributes
 * 
 * Example usage
 * -------------
 * <script src="https://code.jquery.com/jquery-2.2.0.min.js"></script>
 * <script 
 * 	 type="text/javascript" 
 * 	 src="vendor/yellow/Yellow.js"
 * 	 data-main="js/build/build.js" <!-- Location to load built script from -->
 * 	 data-src="js/"	 <!-- Location to load scripts from when they are not included -->
 * 	 data-console="1"  <!-- Whether output should be sent to the console with y.log -->
 * ></script>
 * 
 * 
 * 
 * The following steps are taken on startup
 * 1. The url provided in data-main is loaded 
 * 2. The document is scanned for html elements that have attribute y-use
 * 3. Scripts are loaded for all space separated paths that are provided in these html-elements under y-use="path path path"
 * 4. For all elements a definition-instance is created for each provided path
 * 5. the 'start' function is called on all instances
 * 
 * 
 * HTML example snippet
 * --------------------
 * <div y-use="people.List">
 *     <span y-name="header">This is a list</span>
 * </div>
 * 
 * Script example snippet
 * ----------------------
 * define('people.List') // Create e definition under the same name
 * .use('people.Helper') // Use some other script.
 * .use('http://libary', 'globalname') // Use some vendor script. When it registers as a global, pass along the name of the global
 * .as(function(y, helper, external){ // The class that is used for the elemens
 *	this.start = function(scope){ // init function receives jQuery(element) (scope)
 *	
 *	}
 * });
 * 
 * Templates can be defined in two places: In the html or in the definition.
 * 
 * HTMl template definition:
 * ------------------------
 * <div y-use="people.List">
 *      <script type="text/html" y-name="person.html">
 *			<div>
 *				<span>{{firstname}}</span><br />
 *				<span>{{lastname}}</span>
 *			</div>
 *		</script>
 * </div>
 * 
 * 
 * Script template definition
 * When a tempalte is defined in the componenet, the second argument will be a template function
 * to access the defined tempaltes
 * --------------------------
 * define('people.List')
 * .template('person.script' , '\
 * <div>\
 *		<span>{{firstname}}</span><br />\
 *		<span>{{lastname}}</span>
 * </div>')
 * .as(function(y, template){ 
 *	this.init = function(scope){
 *		y.log(scope.template('person.html'));
 *		y.log(template('person.script'));
 *	}
 * });
 * 
 */
(function(document, window, jQuery)
{
	/**
	 * Get executing (this) script node
	 * use currentScript for everythis but IE11: fall back on last script for IE
	 */
	var script =  document.currentScript ? jQuery(document.currentScript) : script = jQuery('script').last();
	
	/**
	 * Config object that gets it's vars from the script html attributes
	 * @type Object
	 */
	var __config = {
		define: script.data('define') || 'define',
		main: script.data('main') || false,
		src: script.data('src') || '',
		console: script.data('console') || false
	};
	
	
	/**
	 * The public yellow object that will be available in the global namespace
	 * under the configured name
	 * Call it with a html element as argument and a jQuery wrapped element will be returned
	 * Loaded script will use the global object to call define() to register themselves
	 * Also helper functions like is[Type](), outer() and log()
	 * 
	 * @type Object
	 */
	var __public = function(element) {
		return jQuery(element);
	};
	
	
	/**
	 * Add Yellow helpers to jQuery
	 * start: start up an element
	 * element: get an element with y-name="name"
	 */
	jQuery.fn.extend({
		
		/**
		 * attach a definition-instance to an alement, so it can be used to call invoke
		 */
		attach: function(instance){
			// get domnode
			var node = this[0];
			// add array with attached instances to the htmlnode
			if(!__public.isSet(node.instances)){
				node.instances = [];
			}		
			// add the instance to the used instances array on the node
			node.instances.push(instance);
			//chainable
			return this;
		},
		
		/**
		* Start up a portion of a document
		* @returns void
		*/
		start: function(handlers){
			// alias for this
			var scope = this;
			
			// add events on elements in scope and scope itself
			var emitters = scope.find('[y-on]');
			if(scope.attr('y-on')) {
				emitters = emitters.add(scope);
			}
			emitters.each(function(){
				// attribute has the form:  click touchstart|stop:dosomething(1) ~ mouseover|stop:dosomethingelse(1 + 4)
				var emitter = jQuery(this);
				var attr = emitter.attr('y-on');
				emitter.removeAttr('y-on');
				var statements = attr.split('~');
				for(var i = 0; i < statements.length; i++) {
					// add handler
					emitter.handler(statements[i], handlers);
				}
			});
				
			// get named elements from scope and scope itself
			// so we can save the original html and make a fresh copy later
			var named = scope.find('[y-name]');
			if(scope.attr('y-name')) {
				named = named.add(scope);
			}
			
			named.each(function(){				
				// save the original html, so we can make a fresh copy later
				this.__html = this.outerHTML;
			});

			// get elements from scope and scope itself
			var use = scope.find('[y-use]');
			if(scope.attr('y-use')) {
				use = use.add(scope);
			}
			
			// the elements by definition path
			var elements = {};
			use.each(function(){
				// save the original html, so we can make a fresh copy later
				this.__html = this.outerHTML;
				// the element
				var element = jQuery(this);
				// get used paths: spaceseparated names
				var paths = element.attr('y-use').split(' ');
				for(var i = 0; i < paths.length; i++){
					var path = paths[i].trim();
					if(path.length > 0){
						// if it doesnt exist, create an array for it
						if(!__public.isSet(elements[path])){
							elements[path] = [];
						}
						// add to the instances dictionary
						elements[path].push(element);
						// add it to the used definitions list
						__loader.add(path);
					}
				}	
			});

			// Tell loader to process the queue
			// and pass a callback function
			__loader.process(function(){
				// loader queue has resolved: 
				// create an instance for each used definition
				// call start on all instances after instantiatiion
				var instances = [];
				
				for(var path in elements){
					// get the definition
					var definition = __public.get(path);
					// check if it exists
					if(!definition){
						throw new Error('Unknown definition: ' + path + '. ')
					}
					// make an instance for all the elements with this name
					for(var i = 0; i < elements[path].length; i++){
						// get element
						var element = elements[path][i];
						// create instance 
						var instance = definition.__instance();
						// attach the definition to the instance so it is invovakable
						element.attach(instance);
									
						// keep track of all the instance / element pairs, so they can be started later
						instances.push({
							instance: instance,
							element: element
						});
					}
				}
				// start all the instances at once
				// if one instance calls invoke on another, this way they will at least all be created at that moment
				// if invoke was called before __init (and therefore before start()), the invoke method will take care of that
				for(var j = 0; j < instances.length; j++){
					instances[j].instance.__init( instances[j].element );
				}
			});
					
			// chainable
			return scope;
		},
		
		
		/**
		 * Add an eventhandler
		 * Will use methods in handler, but will also look at all exposed methods in attached instances up to body
		 * And call the all.
		 * Unless the stop filter is given
		 * 
		 * @param string statement of the form  click touchstart|stop:dosomething(1) or click touchstart|stop:dosomething
		 * @param object handlers named callbacks that can be referenced in the expression
		 */
		handler: function(statement, handlers) {
			// the element that receives the event
			var scope = this;
			
			// retreive the correct parts from the statement
			var parts = statement.split(':');
			var event = parts[0];
			var filters = event.split('|');
			event = filters.shift();
			var expression = __public.isSet(parts[1]) ? parts[1].trim().replace(/\$e/g, 'e').replace(/\$this/g, '__public(scope)') : '';
			var handler = expression.split('(')[0].trim();
			
			// make sure handlers is an object
			if(! __public.isObject(handlers)) {
				handlers = {};
			}
			
			// normalize filters
			var stop = false;
			var prevent = false;
			for(var i = 0; i < filters.length; i++){
				if(filters[i] === 'stop'){
					stop = true;
				}
				if(filters[i] === 'prevent'){
					prevent = true;
				}
			}
			
			// finally, register the event
			scope.on(event, function(e){
				// use filters
				if(stop){
					e.stopPropagation();
				}
				if(prevent){
					e.preventDefault();
				}

				// try to find a function to use as callback
				var fn = null;
				if(__public.isFunction(handlers[handler])) {
					// function is given in the provided handlers
					fn = handlers[handler];
				} else {
					// function not given, traverse up to find a usable function in y-use instances
					var receiver = scope.parents('[y-use]');
					while(receiver.length > 0 && fn === null) {
						if(__public.isArray(receiver[0].instances)) {
							var instances = receiver[0].instances;
							for(var i = 0; i < instances.length; i++){
								if(__public.isFunction(instances[i][handler])){
									fn = instances[i][handler];
									break;
								}
							}
						}
						receiver = receiver.parents('[y-use]');
					}
				}
				if(__public.isFunction(fn)) {
					if(handler !== expression) {
						(function(___fn___) {
							eval ('var ' + handler + ' = ___fn___; ' + expression + ';');
						})(fn);
					} else {
						fn.call(scope, e);
					}
				}
			});
		},
		
		
		/**
		 * Get a html element with y-name attribute
		 * @param string name
		 * @param string method jquery method to use instead of 'find'
		 * @returns element
		 */
		fetch: function(name, method) {
			if(! __public.isSet(name)){
				var found  = this.find('[y-name]:not(script)');
				
				var elements = {};
				found.each(function(index, element){
					element = jQuery(element);
					var names = element.attr('y-name').split(' ');
					for(var i = 0; i < names.length; i++) {
						if(__public.isSet(elements[names[i]])) {
							// add to jquery resultset
							elements[names[i]] = elements[names[i]].add(element);
						} else {
							// add jquery element
							elements[names[i]] = element;
						}
					}
				});
				
				return elements;
			} else {
				if(! __public.isSet(method)){
					method = 'find';
				}
				return this[method]('[y-name~="' + name + '"]:not(script)');
			}
			
		},
		

		/**
		 * Call a method on an element that has a Yellow component instance tied to it
		 * In case of multiple components, the first available method with the name will be called and that's it.
		 * @param string method
		 * @returns mixed
		 */
		invoke : function(method){
			// get the real dom element, as the used array is attached there
			var node = this[0];
			// check if it exists and if there is a 'used' array
			if(__public.isSet(this[0]) && __public.isArray(this[0].instances)){
				// check on all the used instances if there are 
				for(var i = 0; i < node.instances.length; i++){
					// check is there is a method with the supplied name
					if(__public.isFunction(node.instances[i][method])){
						var instance = node.instances[i];
						// call __init first, just to be sure. If it was called before, that's ok, as init will only run once
						// the argument is the element
						instance.__init(this);
						// shift the first argument (the method name)
						var args = Array.prototype.slice.call(arguments);
						args.shift();
						// call the method with the remaining arguments
						return instance[method].apply(instance, args);
					}
				}
			}
		},
		
		
		/**
		 * Get a html contents of a script with the name y-[name]
		 * @param String name
		 * @returns string
		 */
		template: function(name){
			return this.find('script[y-name~="'+name+'"]').html();	
		},
		
		
		/**
		 * Create a copy of an element
		 * @param Booelan start If true is passed, the element will be started automatically
		 */
		make: function(start)
		{
			if(this[0].__html) {
				var element = __public(this[0].__html);
			} else {
				var element = __public(this[0].outerHTML);
			}
			if(start) {
				element.start();
			}
			return element;
		}
	});
	
	

	/**
	 * Properties that will be copied over to the __public object
	 * we could have writen this as __public.prop = ..., but this is shorter
	 * Will be removed after copying
	 * @type Object
	 */
	var properties = {
		/**
		 * Globals
		 */
		document: jQuery(document),
		window: jQuery(window),
		script: script,
		jQuery: jQuery,
		
		/**
		 * Definitions
		 */
		definitions: {},
		
		/**
		 * Create a definition and set it
		 * returns a creator object that can be used to further fill in the definition
		 * @param string path
		 * @returns Object
		 */
		define: function(path){
			// create a new definition
			var definition = new __Definition();
			// store it
			__public.set(path, definition);
			// let the loader know this path was loaded and resolve it.
			// this is used when we load a prcompiled buncle of scripts
			__loader.resolve(path);
			// return definition creator to chain additional commands
			return definition.creator;
		},
		
		/**
		 * Set a definition
		 * @param string path
		 * @param Object definition
		 * @returns void
		 */
		set: function(path, definition) {
			// check if name is ok
			if(!__public.isString(path) || ! /^[a-zA-Z0-9\-_\.\:]+$/.test(path)){
				throw new Error('Trying to define without a valid name: ' + path);
			}
			if(__public.isSet(__public.definitions[path])){
				__public.log('Redefining previously defined ' + path);
			}
			__public.definitions[path] = definition;
		},
		
		/**
		 * Get a definition
		 * @param string path
		 * @returns Object
		 */
		get: function(path) {
			if(__public.isSet(__public.definitions[path])) {
				return __public.definitions[path];
			}
		},
		
		
		/**
		 * Run a definition
		 * @param string path
		 * @returns {undefined}
		 */
		run: function(path) {
			// add the path to the loader
			__loader.add(path);
			// process the queue
			__loader.process(function(){
				// get the definition
				var definition = __public.get(path);
				// check if it exists
				if(!definition){
					throw new Error('Unknown definition: ' + path + '. ')
				}
				// create instance
				var instance = definition.__instance();
				// get extra arguments passed to run
				var args = Array.prototype.slice.call(arguments);
				args.shift();
				// call the __init method with the remaining arguments and return the result
				instance.__init.apply(instance, args);
			});
		},
		
		
		/**
		 * Get outer yellow instance
		 * @returns {window}
		 */
		outer: function() {
			var traverse = window;
			var outer = window;
			// walk through parents to find outermost window with yellow defined
			// if one is found, use that as yellow
			while(traverse.parent.location !== traverse.location){
				traverse = traverse.parent;
				if(traverse.globalYellowInstance !== null){
					outer = traverse;
				}
			}
			return outer.globalYellowInstance;
		},
		
		/**
		* Testers for value type
		*/
		isString: function(mixed) {
			return this.isType(mixed,'[object String]');
		},
		isArray: function(mixed){
			return this.isType(mixed,'[object Array]');
		},
		isPlainObject: function(mixed){	
			if (typeof mixed == 'object' && mixed !== null) {
				if (typeof Object.getPrototypeOf == 'function') {
					var proto = Object.getPrototypeOf(mixed);
					return proto === Object.prototype || proto === null;
				}
				return Object.prototype.toString.call(mixed) == '[object Object]';
			}
			return false;
		},
		isObject: function(mixed){
			if(this.isSet(mixed) === false){
				return false;
			} else {
				return this.isType(mixed,'[object Object]');
			}
		},
		isFunction: function(mixed){
			return this.isType(mixed,'[object Function]');
		},
		isNumeric: function(mixed){
			return !isNaN(mixed);
		},
		isNumber: function(mixed){
			return this.isType(mixed,'[object Number]');
		},
		isInt: function(mixed){
			return !isNaN(parseInt(mixed,10)) && (parseFloat(mixed,10) === parseInt(mixed,10));
		},
		isFloat: function(mixed){
			return this.isNumber(mixed) === true && this.isInt(mixed) === false;
		},
		isSet: function(mixed){
			return !(typeof mixed === 'undefined' || mixed === null);
		},
		isNull: function(mixed){
			return mixed === null;
		},
		isType: function(mixed, type) {
			return Object.prototype.toString.call( mixed ) === type;
		},

	   	/**
		* Helper: log a variable to console
		* @param {mixed} variable
		* @returns {void}
		*/
	   log: function(variable, showLineNr) {
		   if(__config.console && window.console && window.console.log){
			    window.console.log(variable);
			   if(showLineNr !== false){
				   var error = new Error();
				   if(error.stack){
					    window.console.log(error.stack.split("\n")[2]);
				   }
			   }
		   }
	   },
	   ajax: jQuery.ajax
	};
	
	// copy over the properties to yellow and remove var
	for(var name in properties){
		__public[name] = properties[name];
	}
	properties = null;


	/**
	 * Loader object that loads scripts
	 */
	var __loader = {
		
		// the queue that holds paths that should be loaded
		queue: [],
		
		// object that holds paths that are still loading
		pending: {},
		
		// object that holds loaded paths
		loaded: {},
		
		/**
		 * load a single script from an url, call done when done
		 * @param string url
		 * @param function done
		 * @returns void
		 */
		load: function(url, done){
			// create script tag to load the script
			var parent = document.getElementsByTagName('body')[0];
			var script = document.createElement('script');
			script.src = url;
			script.setAttribute('async', false);
			// callback for the script load
			var callback = function(result){
				//help garbage collection
				script.onload = null;
				script.onerror = null;
				script.onreadystatechange = null;
				script.ontimeout = null;
				parent.removeChild(script);
				// call callbacks
				if(__public.isFunction(done)){
					done(result);
				}
			};
			// add callback
			if(script.addEventListener){
				// Modern browsers
				script.onload = function(){
					callback('done');
				};
				script.onerror = function(){
					callback('fail');
				};
			} else if(script.readyState) {
				// IE 8-
				script.onreadystatechange = function(){
					if(script.readyState == 'loaded' || script.readyState == 'complete'){
						callback('done');
					}
				};
				script.ontimeout = function(){
					callback('fail');
				};
			}
			// add script to the page to start loading
			parent.appendChild(script);
		},
		
		/**
		 * Add a path to the queue
		 * 
		 * @param string path
		 * @param string globalName when using an extrernal library, there will probably be a global var available to use
		 * @returns void
		 */
		add: function(path){
			__loader.queue.push(path);
		},
		
		/**
		 * Process the queue
		 * @param function done
		 * @returns void
		 */
		process: function(done){
			// load elements still in the queue
			while(__loader.queue.length > 0) {
				var path = __loader.queue.shift();
				if(! __loader.loaded[path] && ! __loader.pending[path]){
					
					// start loading: add this element to the pending scripts
					__loader.pending[path] = true;
					if(path.indexOf('http://') === 0 || path.indexOf('https://') === 0 || path.indexOf('//') === 0){
						// absolute url given
						var src = path;
					} else {
						// dotted path given: create a url
						var src = __config.src + path.split('.').join('/') + '.js'
					}
		
					// go get it
					__loader.load(src, (function(p){
						return function(result) {
							if(result === 'fail') {
								throw new Error('Failed to load script: ' + p);
							}
							// resolve path
							__loader.resolve(p);

							// try processing the loader again
							__loader.process(done);
						};
					})(path));
				} else if(__loader.loaded[path]) {
					// path was already loaded before: resolve it.
					__loader.resolve(path);
				}
			}
			
			// check if there are pending files
			var pending = false;
			for(var i in __loader.pending){
				if(__loader.pending[i] === true){
					pending = true;
					break;
				}
			}
			
			// no pending files: callback!
			if(! pending) {
				done();
			}
		},
		
		/**
		 * Remove a path from pending and add it to loaded
		 * @param {type} path
		 * @returns {undefined}
		 */
		resolve: function(path){
			// remove this path from pending
			delete __loader.pending[path];
			// set it to loaded instead, so we dont load it twice.
			__loader.loaded[path] = true;
		}
	};


	/**
	 * A definition instance contains an object called 'creator'
	 * When __public.define is called, a new definition is created and the creator object is returned.
	 * A creator object is used to add dependencies, templates, and static properties to the definition
	 * Lastly the .as function should be called to finalize the definition.
	 * 
	 * When a the argument for 'as' is a function, a call to .make will reutn a new instance of the function
	 * after that, the 'init' function will be called on the new instance, if available with the supplied argumens
	 * 
	 * @returns Object
	 */
	var __Definition = function()
	{
		// array with dependencies to load
		var _use = [];
		
		// templates
		var _templates = {};
		
		// the public definition
		// only contains a make function
		// but will receive additional properties while defining 
		var _definition = {
			
			// this yellow object for use in static definitions as this.yellow or this.y
			y: __public,
			yellow: __public,
			
			// make templates available in defintitions as this.template()
			template: function(name){
				if(__public.isSet(_templates[name])){
					return _templates[name];
				}
			},
			
			/**
			 * Set of creator functions that allow modules to define themselves
			 */
			creator: {
				
				/**
				* set dependencies
				*/
				use: function(path, globalName) {
					// add it to the use array
					_use.push([path, globalName]);
					// chainable
					return this;
				},
				
				/**
				* Set static vars & methods
				*/
				set: function(object) {
					if(! __public.isObject(object)){
						// check if static data is valid
						throw  new Error('Trying to set invalid data: ' + object);
						return;
					}
					// copy over properties
					for(var i in object){
						_definition[i] = object[i];
					}
					// chainable
					return this;
				},
				
				
				/**
				* Set template 
				*/
				template: function(name, template) {
					// store template under name
					_templates[name] = template;
					// chainable
					return this;
				},
			
				/**
				* This is the closing call for a definition
				* Either pass an object with additional properties or a constructor function
				* no extra calls, so not chainable
				* Cleanup & load dependencies afterwards
				*/
				as: function(definition) {
					
					if(__public.isFunction(definition)){
						// create an __instance method to create an instance
						_definition.__instance = function() {
							// variable arguments for constructor.
							// always start with yellow
							var args = [null, __public];
							
							// add dependencies
							for(var i = 0; i < _use.length; i++){
								if(__public.isString(_use[i][1])){
									// a global name was given: 
									// this is a vendor file that registers under a global name
									args.push(window[_use[i][1]]);
								} else {
									args.push(__public.get(_use[i][0]));
								}
							}
							
							// add template function if there are templates
							if(Object.keys(_templates).length > 0){
								args.push(_definition.template)
							}
							
							// add the defintion itself as last argument, so we have access to static vars
							args.push(_definition);
							
							
							// create instance with variable arguments
							// check StackOverflow for how this works
							var instance = new (Function.prototype.bind.apply(definition, args));
							
							// add init function that calls start and cleans up start itself
							instance.__init = function() {
								if(__public.isFunction(instance.start)){
									// get the function
									var fn = instance.start;
									// start can only run once. so remove it
									instance.start = null;
									// pass along arguments that were given to __init()
									fn.apply(instance, arguments);
								}
							};
							
							return instance;
						};
						
						// convenient shortcut to call __instantiate() and __init() in order
						_definition.make = function() {
							// create instance
							var instance = _definition.__instance();
							// pass along arguments that were given to make()
							instance.__init.apply(null, arguments);
							// return it
							return instance;
						};
						
					} else if(__public.isObject(definition)){
						// copy over extra stuff from definition to _definition
						for(var i in definition){
							_definition[i] = definition[i];
						}
					} else {
						// error
						throw new Error('Trying to define without a valid constructor or object');
					}

					// remove creator object
					delete _definition.creator;
					
					// load dependencies defined in 'use'
					// by adding the to the loader queue
					for(var i = 0; i < _use.length; i++){
						__loader.add(_use[i][0], _use[i][1]);
					}
					
					// make define.as. chainable
					return __public;
				}
			}
		};
		return _definition;
	};
	

	// make a public define function that calls __public.define
	window.globalYellowInstance = __public;
	window[__config.define] = function(name){
		return __public.define(name)
	};
	
	// error handler
	window.addEventListener('error', function (e) {
		e.preventDefault();
		var message = ''+e.filename+':' + e.lineno + ': ' + e.message;
		__public.log(message, false);
	});


	if(__config.main){
		// load main if one was given
		__loader.load(__config.main, function(){
			// when done, process the dependencies set by main
			__loader.process(function(){
				// when that is done, start app with document as the scope 
				__public(document).start();
			});
		});
	} else {
		// just start it, when no main was given
		__public(document).start();
	}
	
	// make chainable
	return __public;
})(document, window, jQuery)