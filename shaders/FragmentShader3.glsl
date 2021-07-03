#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragPos;
in vec3 fragNormal;
out vec4 outColor;
uniform float textureRate;
uniform int nofLights;
uniform sampler2D normalMap;

#define NUMBER_OF_MAX_LIGHTS 5
//#define LIST (0,1)

uniform float lightParameters[NUMBER_OF_MAX_LIGHTS*17];
uniform mat4 lightsViewSpaces[NUMBER_OF_MAX_LIGHTS];
uniform mat4 lightsProjSpaces[NUMBER_OF_MAX_LIGHTS];
uniform sampler2D lightsShadowMaps[NUMBER_OF_MAX_LIGHTS];



#define TYPE 0
#define POS_X 1
#define POS_Y 2
#define POS_Z 3
#define COL_R 4
#define COL_G 5
#define COL_B 6
#define COL_A 7
#define INTENSITY 8
#define SPECULAR_STREGTH 9
#define CAM_X 10
#define CAM_Y 11
#define CAM_Z 12
#define CUTOFF 13
#define DIR_X 14
#define DIR_Y 15
#define DIR_Z 16
#define SHADOW_STATUS 17


//textures
uniform sampler2D tex1;
uniform sampler2D tex2;

//shadow
uniform sampler2D shadowMap;
uniform mat4 lightProjSpace;
uniform mat4 lightViewSpace;

uniform int normalMapStat;


float calculateShadow(vec4 fragPosLightSpace, int i)
{
    float shadow = 0.0;

    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;

    //There is a problem while using unconstant indexs for sampler2D list
    //for example there is a list: sampler2d lstSampler2D[10];
    //Then lstSampler[0] works well but,
    //int a = 0;  lstSampler[a] does not work
    //I tried to change the version of glsl to 460 but I can't after some trials
    //After that I just added switch statement the solve the problem, it is a solution
    //But it's not good coding. The problem might be my opengl version
    //but I used  opengl and python versions which are recomended on LMS.
    float closestDepth= 0.0;
    switch (i) {
    case 0:
        closestDepth = texture(lightsShadowMaps[0], projCoords.xy).r; break;
    case 1:
        closestDepth = texture(lightsShadowMaps[1], projCoords.xy).r; break;
    case 2:
        closestDepth = texture(lightsShadowMaps[2], projCoords.xy).r; break;
    }
    //closestDepth = texture(lightsShadowMaps[0], projCoords.xy).r;

    float currentDepth = projCoords.z;

    vec2 texelSize = vec2(0,0);
    switch (i) {
    case 0:
        texelSize = 2.0 / textureSize(lightsShadowMaps[0], 0); break;
    case 1:
        texelSize = 2.0 / textureSize(lightsShadowMaps[1], 0); break;
    case 2:
        texelSize = 2.0 / textureSize(lightsShadowMaps[2], 0); break;
    }
    //vec2 texelSize = 2.0 / textureSize(lightsShadowMaps[0], 0);


    for (int x = -1; x <= 1; ++x)
    {
        for (int y = -1; y <= 1; ++y)
        {
            float pcfDepth = 0.0;
            switch (i) {
                case 0:
                    pcfDepth = texture(lightsShadowMaps[0], projCoords.xy + vec2(x, y) * texelSize).r; break;
                case 1:
                    pcfDepth = texture(lightsShadowMaps[1], projCoords.xy + vec2(x, y) * texelSize).r; break;
                case 2:
                    pcfDepth = texture(lightsShadowMaps[2], projCoords.xy + vec2(x, y) * texelSize).r; break;
                }
            //pcfDepth = texture(lightsShadowMaps[0], projCoords.xy + vec2(x, y) * texelSize).r;

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

    //normal mapping
    vec3 normal = texture(tex2, fragUV).rgb;
    normal = normalize(normal * 2.0 - 1);
    normal = normal * 0.5 + 0.5 ;
    vec3 normalSpec = 1 - normal;
    //normal = 1 - normal;

    float specIntensity = 3;
    if (normalMapStat != 1) {
        normal = fragNormal;
        normalSpec = normal;
        specIntensity = 300.0;
    }

    vec4 light = vec4(0,0,0,0);
    //Check nofLights part
    for (int i = 0; i < nofLights  ; i++){

        int light_i = ((i) * 18);

        //ambient
        float ambientStrength = 0.05;
        vec4 lightColor = vec4(lightParameters[light_i+COL_R],lightParameters[light_i+COL_G], lightParameters[light_i+COL_B], lightParameters[light_i+COL_A]);
        vec4 ambient = lightParameters[light_i+SPECULAR_STREGTH] * lightColor;

        vec3 norm = normalize(normal);
        vec3 lightPos = vec3(lightParameters[light_i+POS_X],lightParameters[light_i+POS_Y],lightParameters[light_i+POS_Z]);
        vec3 lightDir = normalize(lightPos - fragPos);
        float lightDistance = length(lightPos - fragPos);

        vec4 diffuse = vec4(0,0,0,0);
        vec4 specular = vec4(0,0,0,0);
        float intensity = 0.0;
        float shadow = 1.0;
        // SPOTLIGHT
        if (lightParameters[light_i+TYPE] == 1){
            vec3 direction1 = vec3(lightParameters[light_i+DIR_X],lightParameters[light_i+DIR_Y],lightParameters[light_i+DIR_Z]);
            float theta = dot(lightDir, normalize(-direction1));
            float cutOff2 = radians(lightParameters[light_i+CUTOFF]);
            vec4 light1 = vec4(0, 0, 0, 0);
            if (theta > cutOff2)
            {
                float outerCutOff = radians(lightParameters[light_i+CUTOFF] + 1);
                float epsilon   = (-cutOff2 + outerCutOff);//
                intensity = clamp((theta - outerCutOff) / epsilon, 0.0, 1.0);
                // simple lambert diffuse shading model
                float diff = max(dot(norm, lightDir), 0.0);
                diffuse = diff * lightColor;

                //Blinn's specular shading model

                vec3 viewDir    = normalize(vec3(lightParameters[light_i+CAM_X],lightParameters[light_i+CAM_Y],lightParameters[light_i+CAM_Z]) - fragPos);
                vec3 halfwayDir = normalize(lightDir + viewDir);
                float spec = pow(max(dot(normalSpec, halfwayDir), 0.0), specIntensity);
                specular = lightColor * spec * lightParameters[light_i+SPECULAR_STREGTH];



                if (lightParameters[light_i + SHADOW_STATUS] == 1.0) {
                        //shadow
                        vec4 FragPosLightSpace = lightsProjSpaces[i]*lightsViewSpaces[i]*vec4(fragPos, 1.0);
                        shadow = calculateShadow(FragPosLightSpace, i);

                }


            }
            light += (diffuse + specular) * 2* lightParameters[light_i+INTENSITY] * intensity* shadow;
        }
        if (lightParameters[light_i+ TYPE] == 0){

            // simple lambert diffuse shading model
            float diff = max(dot(norm, lightDir), 0.0);
            diffuse = diff * lightColor;

            //Blinn's specular shading model
            vec3 viewDir    = normalize(vec3(lightParameters[light_i+CAM_X], lightParameters[light_i+CAM_Y], lightParameters[light_i+CAM_Z]) - fragPos);
            vec3 halfwayDir = normalize(lightDir + viewDir);
            float spec = pow(max(dot(normalSpec, halfwayDir), 0.0), specIntensity);
            specular = lightColor * spec * lightParameters[light_i+SPECULAR_STREGTH];

            light += (diffuse + specular)* lightParameters[light_i+INTENSITY] ;

        }

    }

    outColor = light* (texVal*(1-textureRate) + texVal2*textureRate);

}


