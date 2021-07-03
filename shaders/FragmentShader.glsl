#version 330
in vec4 fragColor;
in vec2 fragUV;
in vec3 fragPos;
in vec3 fragNormal;
out vec4 outColor;
uniform float textureRate;



//LIGHT2
//difuse
uniform vec3 lightPos1;
uniform vec4 lightColor1;
uniform float lightIntensity1;

//specular
uniform vec3 viewPos1;
uniform float specularStrength1;

//LIGHT1
//difuse
uniform vec3 lightPos2;
uniform vec4 lightColor2;
uniform float lightIntensity2;

//specular
uniform vec3 viewPos2;
uniform float specularStrength2;

//textures
uniform sampler2D tex1;
uniform sampler2D tex2;

void main()
{
	vec4 texVal = texture(tex1, fragUV);
	vec4 texVal2 = texture(tex2, fragUV);

	//ambient
	float ambientStrength = 0.05;
	vec4 lightColor = vec4(1,1,1,0);
    vec4 ambient = ambientStrength * lightColor;


	// simple lambert diffuse shading model
	vec3 norm = normalize(fragNormal);
	vec3 lightDir = normalize(lightPos1 - fragPos);
	float diff = max(dot(norm, lightDir), 0.0);
	vec4 diffuse1 = diff * lightColor1;
	
	//Blinn's specular shading model
	vec3 viewDir    = normalize(viewPos1 - fragPos);
	vec3 halfwayDir = normalize(lightDir + viewDir);
	float spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 300.0);
	vec4 specular1 = lightColor1 * spec * specularStrength1;

    vec4 light1 = (diffuse1 + specular1) * lightIntensity1;

	// simple lambert diffuse shading model
	lightDir = normalize(lightPos2 - fragPos);
	diff = max(dot(norm, lightDir), 0.0);
	vec4 diffuse2 = diff * lightColor2;

	//Blinn's specular shading model
	viewDir    = normalize(viewPos2 - fragPos);
	halfwayDir = normalize(lightDir + viewDir);
	spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 300.0);
	vec4 specular2 = lightColor2 * spec * specularStrength2;
	
	vec4 light2 = (diffuse2 + specular2) * lightIntensity2;

	float nDotL = max(dot(fragNormal, lightDir), 0.0);
	outColor = fragColor * (ambient + light1 + light2) * (texVal*(1-textureRate) + texVal2*textureRate);
}
