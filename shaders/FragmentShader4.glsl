#version 330
in vec4 fragColor;
in vec2 fragUV;
in vec3 fragPos;
in vec3 fragNormal;
out vec4 outColor;
uniform float textureRate;


//LIGHT1 - SPOT LIGHT
uniform vec3  direction;
uniform float cutOff;
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

//shadow
uniform sampler2D shadowMap;
uniform mat4 lightProjSpace;
uniform mat4 lightViewSpace;


float calculateShadow(vec4 fragPosLightSpace)
{


    // perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    // get closest depth value from light's perspective (using [0,1] range fragPosLight as coords)
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    // check whether current frag pos is in shadow
    float shadow = currentDepth > closestDepth  ? 0.0 : 1.0;

    //PCF: To provide a smooth transition from shadow to lighted fragments
    shadow = 0.0;
    vec2 texelSize = 2.0 / textureSize(shadowMap, 0);
    for (int x = -1; x <= 1; ++x)
    {
        for (int y = -1; y <= 1; ++y)
        {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r;
            shadow += currentDepth > pcfDepth ? 0.0 : 1.0;
        }
    }
    shadow /= 9.0;

    return shadow;
}


void main()
{
    vec4 texVal = texture(tex1, fragUV);
    vec4 texVal2 = texture(tex2, fragUV);

    //ambient
    float ambientStrength = 0.05;
    vec4 lightColor = vec4(1, 1, 1, 0);
    vec4 ambient = ambientStrength * lightColor;

    //LIGHT 1 - SPOT LIGHT

    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos1 - fragPos);
    float lightDistance = length(lightPos1 - fragPos);


    //float cutOff2 = 1.0;
    float theta = dot(lightDir, normalize(-direction));
    //theta = theta * (3.14/180);
    //theta =  (theta*180)/(3.14);
    float cutOff2 = radians(cutOff);
    vec4 light1 = vec4(0, 0, 0, 0);
    if (theta > cutOff2)
    {
        float outerCutOff = radians(cutOff + 1);
        float epsilon   = (-cutOff2 + outerCutOff);//
        float intensity = clamp((theta - outerCutOff) / epsilon, 0.0, 1.0);
        // simple lambert diffuse shading model
        float diff = max(dot(norm, lightDir), 0.0);
        vec4 diffuse1 = diff * lightColor1;

        //Blinn's specular shading model
        vec3 viewDir    = normalize(viewPos1 - fragPos);
        vec3 halfwayDir = normalize(lightDir + viewDir);
        float spec = pow(max(dot(fragNormal, halfwayDir), 0.0), 300.0);
        vec4 specular1 = lightColor1 * spec * specularStrength1;

        light1 = (diffuse1 + specular1) * 2* lightIntensity1 * intensity;
    }


    //LIGHT 2
    // simple lambert diffuse shading model
    lightDir = normalize(lightPos2 - fragPos);
    float diff2 = max(dot(norm, lightDir), 0.0);
    vec4 diffuse2 = diff2 * lightColor2;

    //Blinn's specular shading model
    vec3 viewDir2    = normalize(viewPos2 - fragPos);
    vec3 halfwayDir2 = normalize(lightDir + viewDir2);
    float spec2 = pow(max(dot(fragNormal, halfwayDir2), 0.0), 300.0);
    vec4 specular2 = lightColor2 * spec2 * specularStrength2;

    vec4 light2 = (diffuse2 + specular2) * lightIntensity2;

    float nDotL = max(dot(fragNormal, lightDir), 0.0);


    //shadow
    vec4 FragPosLightSpace = lightProjSpace*lightViewSpace*vec4(fragPos, 1.0);
    float shadow = calculateShadow(FragPosLightSpace);


    outColor = fragColor * (ambient + light2 + light1 *  shadow) * (texVal*(1-textureRate) + texVal2*textureRate);

}


