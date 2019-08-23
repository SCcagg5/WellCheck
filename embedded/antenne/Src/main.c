/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "usart.h"
#include "gpio.h"
#include <stdlib.h>
#include <string.h>

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

// Turbidity PA6
uint16_t adc1Value = 0;

// Photo-transistor PA7
uint16_t adc2Value = 0;

// Humidity PC10
uint16_t adc3Value = 0;

//appui bouton bleu
char blueButton = 0;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

// cette calback est appelee pour toute interruption par les gpios, et transmet en parametre de quel pin elle vient
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	switch (GPIO_Pin)
	{
		case GPIO_PIN_13:
				blueButton = 1;
	}
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */

int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */
  
  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_UART4_Init();
  MX_ADC1_Init();
  MX_ADC2_Init();
  MX_ADC3_Init();
  
	/* USER CODE BEGIN 2 */
	
	unsigned char *frameData;
	frameData = malloc(3 * sizeof(uint16_t));
	memset(frameData, 0, 3 * sizeof(uint16_t));
	
	//HAL_Delay(3000);

  /* USER CODE END 2 */

  /* Infinite loop */
	while (1)
  {
		/* USER CODE BEGIN WHILE */

		if (blueButton == 1)
		{
			HAL_ADC_Start(&hadc1);
			HAL_ADC_PollForConversion(&hadc1, 100);
		
			HAL_ADC_Start(&hadc2);
			HAL_ADC_PollForConversion(&hadc2, 100);
		
			HAL_ADC_Start(&hadc3);
			HAL_ADC_PollForConversion(&hadc3, 100);
		
			adc1Value = HAL_ADC_GetValue(&hadc1);
			adc2Value = HAL_ADC_GetValue(&hadc2);
			adc3Value = HAL_ADC_GetValue(&hadc3);
			
			*frameData = adc1Value;
			*frameData = *frameData << sizeof(uint16_t);
			
			*frameData += adc2Value;
			*frameData = *frameData << sizeof(uint16_t);
			
			*frameData += adc3Value;
			*frameData = *frameData << sizeof(uint16_t);
		
			sendSigfoxFrame(frameData,sizeof( 3 * sizeof(uint16_t)),0,0);

			//AT command : send_frame [hexData] [nbRepetition] [flag dowlink --> 0 : pas de dl, 1 : dl]
			/*
				Decoder expected frame
				"Downlink" :    (self._trame, 0b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
				"Turbidity" :   (self._trame, 0b011111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
				"GPSLat" :      (self._trame, 0b000000000000111111111111111111110000000000000000000000000000000000000000000000000000000000000000),
				"Acceleration" :(self._trame, 0b000000000000000000000000000000001110000000000000000000000000000000000000000000000000000000000000),
				"GPSLong" :     (self._trame, 0b000000000000000000000000000000000001111111111111111111000000000000000000000000000000000000000000),
				"GPSLongSign" : (self._trame, 0b000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000),
				"GPSlatSign" :  (self._trame, 0b000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000),
				"pH" :          (self._trame, 0b000000000000000000000000000000000000000000000000000000001111111000000000000000000000000000000000),
				"InnerWater" :  (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000),
				"Pression" :    (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000011111111111110000000000000000000),
				"Conductance" : (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000000000000000001111111111100000000),
				"Temperature" : (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111110),
				"OuterWater" :  (self._trame, 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
			*/

			blueButton = 0;
			memset(frameData, 0, 3 * sizeof(uint16_t));
		}
	/* USER CODE END WHILE */
  }
	
	/* USER CODE BEGIN 3 */
  
	/* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage 
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
