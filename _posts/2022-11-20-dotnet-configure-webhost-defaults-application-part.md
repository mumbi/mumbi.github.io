---
title: .NET IHostBuilder.ConfigureWebHostDefaults() 와 ApplicationPart
categories: csharp
tags: ["csharp", "WebHost", "ApplicationPart", "ApplicationName"]
---

# 개요

`IHostBuilder.ConfigureWebHostDefaults()` 를 사용하여 `WebHost` 를 구성할 때 유의해야 하는 점을 소개합니다.

# `IHostBuilder.ConfigureWebHostDefaults()`

| version | method |
| ------- | ------ |
| `ASP.NET Core 2.x` | `WebHost.CreateDefaultBuilder()` |
| `ASP.NET Core 3.x` | `Host.CreateDefaultBuilder()` |
| `.NET 5` | `Host.CreateDefaultBuilder()` |
| `.NET 6` | `WebApplication.CreateBuilder()` |

`ConfigureWebHostDefaults()` 는 `.NET 5` 에서 `Generic Host` 를 지원하면서 추가된 메소드입니다.

`.NET 6` 의 `WebApplication` 은 `ConfigureWebHostDefaults()` 을 래핑한 간단 버전입니다.

## `ASP.NET Core` 프로젝트 생성

```bash
dotnet new web -o WeatherForecast
```

## 기본 코드 작성

Program.cs
```c#
var hostBuilder = Host.CreateDefaultBuilder(args)
    .ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.ConfigureServices((ctx, services) =>
            {
                services.AddControllers();
            });

            webBuilder.Configure((ctx, app) => 
            {
                app.UseRouting();

                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/", () => ctx.HostingEnvironment.ApplicationName);
                    endpoints.MapControllers();
                });
            });
        });

var host = hostBuilder.Build();
host.Run();
```

WeatherForecast.cs
```c#
namespace WeatherForecast;

public class WeatherForecast
{
    public DateTime Date { get; set; }

    public int TemperatureC { get; set; }

    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);

    public string? Summary { get; set; }
}
```

Controllers/WeatherForecastController.cs
```c#
using Microsoft.AspNetCore.Mvc;

namespace WeatherForecast.Controllers;

[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    private readonly ILogger<WeatherForecastController> _logger;

    public WeatherForecastController(ILogger<WeatherForecastController> logger)
    {
        _logger = logger;
    }

    [HttpGet(Name = "GetWeatherForecast")]
    public IEnumerable<WeatherForecast> Get()
    {
        return Enumerable.Range(1, 5).Select(index => new WeatherForecast
        {
            Date = DateTime.Now.AddDays(index),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = Summaries[Random.Shared.Next(Summaries.Length)]
        })
        .ToArray();
    }
}
```

실행
```bash
dotnet run
```

확인
```bash
[mumbi@home ~]$ curl localhost:5061/weatherforecast
[{"date":"2022-11-27T14:03:20.863756+09:00","temperatureC":14,"temperatureF":57,"summary":"Warm"},{"date":"2022-11-28T14:03:20.8637653+09:00","temperatureC":-10,"temperatureF":15,"summary":"Bracing"},{"date":"2022-11-29T14:03:20.8637657+09:00","temperatureC":17,"temperatureF":62,"summary":"Freezing"},{"date":"2022-11-30T14:03:20.863766+09:00","temperatureC":5,"temperatureF":40,"summary":"Bracing"},{"date":"2022-12-01T14:03:20.8637662+09:00","temperatureC":54,"temperatureF":129,"summary":"Scorching"}]
```

컨트롤러가 잘 동작하는 것을 확인할 수 있습니다.

# 라이브러리로 모듈 분리

그런데 `ConfigureWebHostDefaults()` 부분을 다른 애플리케이션에서도 사용하게 되었네요. 

코드를 복사해서 사용할 수 있겠지만, 코드의 중복을 피하기 위해 라이브러리로 분리할 수 있습니다.

## 라이브러리 프로잭트 생성

```bash
dotnet new classlib -o Lib
```

`ASP.NET Core` 를 사용하기 위해 `AspNetCore` 프레임워크를 추가합니다.

Lib.csproj
```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <FrameworkReference Include="Microsoft.AspNetCore.App" />
  </ItemGroup>

</Project>
```

## 모듈 분리

`ConfigureWebHostDefaults()` 를 확장 메소드를 사용하여 제공합니다.

HostBuilderExtensions.cs
```c#
namespace Lib;

using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public static class HostBuilderExtensions
{
    public static IHostBuilder ConfigureMyWebHost(this IHostBuilder hostBuilder)
    {
        return hostBuilder.ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.ConfigureServices((ctx, services) =>
            {
                services.AddControllers();
            });

            webBuilder.Configure((ctx, app) => 
            {
                app.UseRouting();

                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/", () => ctx.HostingEnvironment.ApplicationName);
                    endpoints.MapControllers();
                });
            });
        });
    }
}
```

## 라이브러리 참조

`WeatherForecast` 프로젝트에서 `Lib` 프로젝트를 참조합니다.

```bash
dotnet add reference ../Lib/Lib.csproj
```

## 라이브러리 함수 사용

`WeatherForecast` 에서 분리한 모듈의 함수를 사용합니다.

Program.cs
```c#
using Lib;

var hostBuilder = Host.CreateDefaultBuilder(args)
    .ConfigureMyWebHost();

var host = hostBuilder.Build();
host.Run();
```

실행 및 확인

```bash
[mumbi@home ~]$ curl -i localhost:5061/weatherforecast
HTTP/1.1 404 Not Found
Content-Length: 0
Date: Sat, 26 Nov 2022 05:44:03 GMT
Server: Kestrel
```

????

해당 URL 을 찾을 수 없다고 합니다.

즉, `WeatherForecastController` 가 라우터에 등록되지 않은 것입니다.

원인은 `AddControllers()` 가 코드가 포함된 어셈블리에 있는 컨트롤러들만 추가하기 때문입니다.

# 해결책

등록되어야 할 컨틑롤러와 `AddControllers()` 의 어셈블리가 다르면 컨트롤러를 찾을 수 없기 때문에 찾을 수 있도록 정보를 제공해줘야 합니다.

## `ApplicationPart`

`AddApplicationPart()` 는 `IMvcBuilder` 가 컨트롤러를 찾을 때 추가로 찾을 어셈블리를 추가합니다.

`Lib` 프로젝트의 HostBuilderExtensions.cs
```c#
namespace Lib;

using System.Reflection;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public static class HostBuilderExtensions
{
    public static IHostBuilder ConfigureMyWebHost(this IHostBuilder hostBuilder, Assembly assembly)
    {
        return hostBuilder.ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.ConfigureServices((ctx, services) =>
            {
                services.AddControllers()
                    .AddApplicationPart(assembly);
            });

            webBuilder.Configure((ctx, app) => 
            {
                app.UseRouting();

                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/", () => ctx.HostingEnvironment.ApplicationName);
                    endpoints.MapControllers();
                });
            });
        });
    }
}
```

`WeatherForecast` 프로젝트의 Program.cs
```c#
using Lib;

using System.Reflection;

var hostBuilder = Host.CreateDefaultBuilder(args)
    .ConfigureMyWebHost(Assembly.GetExecutingAssembly());

var host = hostBuilder.Build();
host.Run();
```

실행 및 확인
```bash
[mumbi@home ~]$ curl -i localhost:5061/weatherforecast
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Sat, 26 Nov 2022 05:59:58 GMT
Server: Kestrel
Transfer-Encoding: chunked

[{"date":"2022-11-27T14:59:58.485063+09:00","temperatureC":8,"temperatureF":46,"summary":"Sweltering"},{"date":"2022-11-28T14:59:58.4850736+09:00","temperatureC":26,"temperatureF":78,"summary":"Cool"},{"date":"2022-11-29T14:59:58.4850744+09:00","temperatureC":8,"temperatureF":46,"summary":"Cool"},{"date":"2022-11-30T14:59:58.4850748+09:00","temperatureC":15,"temperatureF":58,"summary":"Bracing"},{"date":"2022-12-01T14:59:58.4850752+09:00","temperatureC":1,"temperatureF":33,"summary":"Freezing"}]
```

## `HostEnvironment.ApplicationName`

하나의 문제가 더 있습니다. 

`WeatherForecast` 프로젝트의 Program.cs
```c#
using System.Reflection;
using Microsoft.Extensions.Logging;
using Lib;

var loggerFactory = LoggerFactory.Create(loggingBuilder => loggingBuilder.AddConsole());
var logger = loggerFactory.CreateLogger<Program>();

var hostBuilder = Host.CreateDefaultBuilder(args)
    .ConfigureMyWebHost(Assembly.GetExecutingAssembly())
    .ConfigureAppConfiguration((hostBuilderContext, configurationBuilder) =>
    {
        logger.LogInformation($"Application Name: {hostBuilderContext.HostingEnvironment.ApplicationName}");
    });

var host = hostBuilder.Build();
host.Run();
```

이렇게 로그로 `ApplicationName` 을 확인보겠습니다. 

```bash
[mumbi@home WeatherForecast]$ dotnet run
info: Program[0]
      Application Name: Lib
```

`ConfigureWebHostDefaults()` 가 `ApplicationName` 을 포함된 어셈블리의 이름으로 설정합니다.

`ApplicationName` 을 실행 중인 어셈블리 또는 원하는 이름으로 바꾸기 위해서 `IWebHostBuilder.UseSetting(webHostDefaults.ApplicationKey, ...)` 를 사용합니다.

`Lib` 프로젝트의 HostBuilderExtensions.cs
```c#
namespace Lib;

using System.Reflection;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public static class HostBuilderExtensions
{
    public static IHostBuilder ConfigureMyWebHost(this IHostBuilder hostBuilder, Assembly assembly)
    {
        return hostBuilder.ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.ConfigureServices((ctx, services) =>
            {
                services.AddControllers()
                    .AddApplicationPart(assembly);
            });

            webBuilder.Configure((ctx, app) => 
            {
                app.UseRouting();

                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/", () => ctx.HostingEnvironment.ApplicationName);
                    endpoints.MapControllers();
                });
            });

            webBuilder.UseSetting(WebHostDefaults.ApplicationKey, assembly.GetName().Name);
        });
    }
}
```

실행 및 확인
```bash
[mumbi@home WeatherForecast]$ dotnet run
info: Program[0]
      Application Name: WeatherForecast
```

# 마무리

`ASP.NET` 이 버전업을 하면서 사용법은 더욱 간단해지고 있지만, 범용성은 점점 줄고 있는 것 같습니다.

라이브러리를 개발하면서 이것 저것 삽질하면서 내부를 알아 가고 있습니다.

같은 문제를 겪으시는 분들께 도움이 되었으면 좋겠습니다.

감사합니다.